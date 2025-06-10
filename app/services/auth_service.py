from datetime import timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.events import event_publisher
from app.core.security import create_access_token, verify_password
from app.db.database import get_db
from app.models.user import User
from app.repositories.user_repository import user_repository
from app.schemas.user import UserCreate, Token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login")


class AuthService:
    """
    Service for handling authentication logic
    """
    
    async def register_user(self, db: Session, user_in: UserCreate) -> User:
        """
        Register a new user
        """
        # Check if user already exists
        user = user_repository.get_by_email(db, email=user_in.email)
        if user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User with this email already exists",
            )
        
        # Create user in database
        user = user_repository.create(db, user_in=user_in)
        
        # Publish user_registered event
        user_dict = {
            "id": user.id,
            "email": user.email,
            "created_at": user.created_at
        }
        await event_publisher.publish_user_registered(user_dict)
        
        return user
    
    def authenticate_user(self, db: Session, email: str, password: str) -> Optional[User]:
        """
        Authenticate user by email and password
        """
        user = user_repository.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user
    
    def create_user_token(self, user_id: str) -> Token:
        """
        Create access token for user
        """
        access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION_MINUTES)
        access_token = create_access_token(
            subject=user_id, expires_delta=access_token_expires
        )
        return Token(access_token=access_token)
    
    async def get_current_user(
        self, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
    ) -> User:
        """
        Get current authenticated user
        """
        credentials_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(
                token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
            )
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception
        
        user = user_repository.get_by_id(db, user_id=user_id)
        if user is None:
            raise credentials_exception
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
            )
        return user


# Singleton instance
auth_service = AuthService()
