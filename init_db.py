import asyncio
import logging

from app.db.database import Base, engine
# Importación implícita para asegurar que los modelos se registren
import app.models.user  # noqa

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
