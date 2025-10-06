from __future__ import annotations

from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy import text

from .models import Base
from config import get_settings

settings = get_settings()

DATABASE_URL = settings.TEST_DB_URL if getattr(settings, "TESTING", False) else settings.DB_URL

engine = create_async_engine(DATABASE_URL, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with engine.connect() as conn:
        await conn.execute(text("SELECT 1"))


async def reset_sqlite_database() -> None:
    """
    Скидає SQLite-базу до «чистого» стану для тестів:
    дропає всі таблиці та створює їх заново.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def close_db() -> None:
    await engine.dispose()


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


@asynccontextmanager
async def get_db_contextmanager():
    """
    Асинхронний контекст-менеджер, що надає AsyncSession.
    Використовується в тестах:
        async with get_db_contextmanager() as db: ...
    """
    async with AsyncSessionLocal() as session:
        yield session
