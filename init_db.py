import asyncio
import logging
from contextlib import asynccontextmanager

from sqlalchemy import text
from sqlalchemy.exc import ProgrammingError

from app.db.database import Base, engine
from app.models.user import User  # Import all models to register them

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def init_db():
    """
    Initialize database tables if they don't exist.
    """
    logger.info("Creating database tables...")
    try:
        # Create tables
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully!")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")
        raise


if __name__ == "__main__":
    logger.info("Initializing database...")
    asyncio.run(init_db())
    logger.info("Database initialization completed!")
