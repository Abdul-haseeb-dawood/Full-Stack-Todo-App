from app.db.database import engine
from app.db.base import Base
from alembic.config import Config
from alembic import command
import asyncio
import os


async def init_db():
    """Initialize the database tables using Alembic migrations."""
    # Run Alembic migrations to update the database to the latest version
    alembic_cfg = Config("alembic.ini")
    command.upgrade(alembic_cfg, "head")
    print("Database tables updated to the latest version with Alembic migrations!")


if __name__ == "__main__":
    asyncio.run(init_db())