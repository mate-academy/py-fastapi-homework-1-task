from typing import AsyncGenerator
from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.settings import get_settings  # pick your correct settings import
from src.database.base import Base       # pick your correct Base import

settings = get_settings()

DATABASE_URL = f"sqlite+aiosqlite:///{settings.PATH_TO_DB}"

# Async engine and session
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_db() -> None:
    """
    Initialize the database: create all tables.
    Should be called on app startup.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    """
    Close the database connection.
    Should be called on app shutdown.
    """
    await engine.dispose()


@asynccontextmanager
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Provide a database session as an async context manager.
    Usage:
        async with get_db() as session:
            ...
    """
    async with AsyncSessionLocal() as session:
        yield session


async def reset_sqlite_database() -> None:
    """
    Drop all tables and recreate them.
    WARNING: This deletes all existing data.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
