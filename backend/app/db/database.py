from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from app.core.settings import settings
import os

# =========================
# DATABASE ENGINE (ASYNC)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://neondb_owner:npg_Vi0MAbn1SrQe@ep-snowy-cherry-ah8bfctf-pooler.c-3.us-east-1.aws.neon.tech/neondb"
)

engine = create_async_engine(
    DATABASE_URL,
    echo=True,
    connect_args={
        "ssl": True,
        "command_timeout": 60,
        "server_settings": {
            "application_name": "todo-app",
        }
    },
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,  # Verify connections before use
    pool_recycle=300,    # Recycle connections after 5 minutes
)
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
