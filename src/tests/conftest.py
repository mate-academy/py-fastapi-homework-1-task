import pytest_asyncio
from httpx import ASGITransport, AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine

from config import get_settings
from src.database.session import (
    get_db_contextmanager,
    init_db,
    reset_sqlite_database,
    engine,
)
from src.database.populate import CSVDatabaseSeeder
from src.main import app


@pytest_asyncio.fixture(scope="function", autouse=True)
async def reset_db():
    await reset_sqlite_database()
    await init_db()


@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as async_client:
        yield async_client


@pytest_asyncio.fixture(scope="function")
async def db_session():
    """Надає асинхронну сесію бази даних."""
    async with get_db_contextmanager() as session:
        yield session


@pytest_asyncio.fixture(scope="function")
async def seed_database(db_session):
    settings = get_settings()
    seeder = CSVDatabaseSeeder(
        csv_file_path=settings.PATH_TO_MOVIES_CSV,
        db_session=db_session
    )

    if not await seeder.is_db_populated():
        await seeder.seed()

    yield db_session
