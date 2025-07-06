from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.security import get_password_hash
from app.models.user import User
from app.schemas.user import UserCreate


class UserRepository:
    """
    Repository for User model to handle database operations
    """

    def get_by_id(self, db: Session, user_id: UUID) -> Optional[User]:
        """
        Get user by ID
        """
        return db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """
        Get user by email
        """
        return db.query(User).filter(User.email == email).first()

    def get_by_username(self, db: Session, username: str) -> Optional[User]:
        """
        Get user by username
        """
        return db.query(User).filter(User.username == username).first()

    def create(self, db: Session, user_in: UserCreate) -> User:
        """
        Create a new user
        """
        db_user = User(
            email=user_in.email,
            username=user_in.username,
            hashed_password=get_password_hash(user_in.password),
            full_name=user_in.full_name,
            is_active=user_in.is_active,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


# Singleton instance
user_repository = UserRepository()