import asyncio
from loguru import logger

from sqlalchemy.ext.asyncio import AsyncEngine
from app.db.database import engine, Base
from app.models.user import User


async def create_tables(engine: AsyncEngine) -> None:
    """
    Create database tables using SQLAlchemy models
    """
    logger.info("Creating database tables...")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    logger.info("Database tables created successfully")


async def init_db() -> None:
    """
    Initialize database with tables
    """
    try:
        await create_tables(engine)
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


if __name__ == "__main__":
    asyncio.run(init_db())
