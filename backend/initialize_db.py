from app.db.database import engine
from app.db.base import Base
import asyncio


async def init_db():
    """Initialize the database tables."""
    async with engine.begin() as conn:
        # Create all tables defined in the models
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created successfully!")


if __name__ == "__main__":
    asyncio.run(init_db())