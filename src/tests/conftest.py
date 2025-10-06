# src/tests/conftest.py
from __future__ import annotations

import os

import pytest_asyncio
from httpx import ASGITransport, AsyncClient

# ці імпорти ПРАЦЮЮТЬ, якщо:
# - src/config/__init__.py експортує get_settings
# - src/database/__init__.py експортує reset_sqlite_database, get_db_contextmanager, CSVDatabaseSeeder
from config import get_settings
from database import reset_sqlite_database, get_db_contextmanager, CSVDatabaseSeeder
from main import app


# робимо так, щоб у тестах використовувалась тестова БД
@pytest_asyncio.fixture(scope="session", autouse=True)
def _testing_env() -> None:
    os.environ["TESTING"] = "1"


# перед кожним тестом чистимо БД
@pytest_asyncio.fixture(scope="function", autouse=True)
async def reset_db():
    await reset_sqlite_database()


# HTTP-клієнт для запитів до FastAPI
@pytest_asyncio.fixture(scope="function")
async def client():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        yield ac


# Асинхронна сесія БД
@pytest_asyncio.fixture(scope="function")
async def db_session():
    async with get_db_contextmanager() as session:
        yield session


# Наповнення БД тестовими даними (якщо порожня)
@pytest_asyncio.fixture(scope="function")
async def seed_database(db_session):
    settings = get_settings()
    seeder = CSVDatabaseSeeder(csv_file_path=settings.PATH_TO_MOVIES_CSV, db_session=db_session)
    if not await seeder.is_db_populated():
        await seeder.seed()
    yield db_session
