from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import declarative_base
from app.core.config import settings

DATABASE_URL = settings.DATABASE_URL

# -------------------------
# Async engine
# -------------------------
engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    future=True,
)

# -------------------------
# Session factory
# -------------------------
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

# ✅ Alias for background services (scheduler, workers)
async_session_factory = AsyncSessionLocal

# -------------------------
# Base model
# -------------------------
Base = declarative_base()

# -------------------------
# Dependency for FastAPI routes
# -------------------------
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
