from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Optional

from app.db.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse, Token, TokenValidationResponse
from app.services.auth_service import auth_service

router = APIRouter()


@router.post("/signup", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def signup(user_in: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user
    """
    try:
        user = await auth_service.register_user(db, user_in)
        return user
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred: {str(e)}",
        )


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """
    Authenticate user and return JWT token
    """
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return auth_service.create_user_token(str(user.id))


@router.get("/health")
async def health_check():
    """
    Health check endpoint
    """
    return {"status": "ok", "service": "auth-login-signup-service"}


@router.post("/validate", response_model=TokenValidationResponse)
async def validate_token(token_request: TokenValidationRequest, db: Session = Depends(get_db)):
    """
    Validate JWT token
    """
    try:
        user, roles = await auth_service.validate_token(db, token_request.token)
        return TokenValidationResponse(
            valid=True,
            userId=str(user.id),
            roles=roles
        )
    except HTTPException as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e.detail),
            headers={"WWW-Authenticate": "Bearer"}
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Error validating token: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"}
        )
