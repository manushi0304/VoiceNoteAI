import asyncio
import sys
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from httpx import AsyncClient, ASGITransport

from app.core.config import settings
from app.core.database import get_db, AsyncSessionLocal
from app.main import app

# Set the selector event loop policy on Windows to avoid 'Event loop is closed' or 'NoneType has no attribute send' asyncpg bugs.
if sys.platform == "win32":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

pytest_plugins = ("pytest_asyncio",)


@pytest.fixture
def anyio_backend():
    """Instruct anyio to use the standard asyncio backend."""
    return "asyncio"


@pytest.fixture(scope="session")
def event_loop():
    """Create a single, session-wide event loop for tests."""
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="session")
async def test_engine():
    """Create SQLAlchemy async engine for the database."""
    engine = create_async_engine(settings.DATABASE_URL, future=True)
    yield engine
    await engine.dispose()


@pytest_asyncio.fixture
async def db_session() -> AsyncSession:
    """Provide a standard clean database session for direct service testing."""
    return AsyncSessionLocal()


@pytest_asyncio.fixture
async def client() -> AsyncClient:
    """FastAPI Test client with the real clean DB dependency."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac
