import os
from typing import Any, Dict, Optional

from pydantic import PostgresDsn, field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Auth Login/Signup Service"
    API_V1_STR: str = "/auth"
    
    # Security
    JWT_SECRET: str = os.getenv("JWT_SECRET", "super-secret-key-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION_MINUTES: int = 60
    
    # Database
    DATABASE_URL: Optional[PostgresDsn] = os.getenv("DATABASE_URL")
    
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            username=os.getenv("POSTGRES_USER", "auth_user"),
            password=os.getenv("POSTGRES_PASSWORD", "secret"),
            host=os.getenv("POSTGRES_HOST", "localhost"),
            port=os.getenv("POSTGRES_PORT", "5432"),
            path=f"/{os.getenv('POSTGRES_DB', 'auth_db')}",
        )
    
    # CORS
    CORS_ORIGINS: list[str] = ["*"]
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 10
    
    # Message broker
    MESSAGE_BROKER_URL: str = os.getenv("MESSAGE_BROKER_URL", "kafka://localhost:9092")
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
