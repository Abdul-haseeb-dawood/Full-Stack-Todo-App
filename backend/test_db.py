from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text
import asyncio
from app.core.settings import settings

# Use your Neon PostgreSQL database
DATABASE_URL = settings.database_url

async def test_connection():
    try:
        engine = create_async_engine(
            DATABASE_URL,
            connect_args={
                "ssl": "require",
            }
        )

        async with engine.connect() as conn:
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful!")
            print(result.fetchone())

        await engine.dispose()
    except Exception as e:
        print(f"Database connection failed: {e}")

if __name__ == "__main__":
    asyncio.run(test_connection())