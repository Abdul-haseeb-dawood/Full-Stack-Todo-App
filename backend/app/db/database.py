from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings
import os

# =========================
# DATABASE ENGINE (ASYNC)

# Use database URL from settings
DATABASE_URL = settings.database_url

# Configuration for database engine
engine = create_async_engine(DATABASE_URL, echo=True)
# =========================
# ASYNC SESSION
# =========================

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autocommit=False,
    autoflush=False,
)

# =========================
# BASE MODEL
# =========================

Base = declarative_base()

# =========================
# DEPENDENCY
# =========================

async def get_async_session() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
