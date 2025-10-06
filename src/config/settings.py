from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


SRC_DIR = Path(__file__).resolve().parents[1]
DB_PATH = SRC_DIR / "database" / "source" / "movies.db"
TEST_DB_PATH = SRC_DIR / "database" / "source" / "test_movies.db"


class Settings(BaseSettings):
    TESTING: bool = False
    DB_URL: str = f"sqlite+aiosqlite:///{DB_PATH}"
    TEST_DB_URL: str = f"sqlite+aiosqlite:///{TEST_DB_PATH}"

    # конфіг Pydantic v2 для BaseSettings
    model_config = SettingsConfigDict(
        env_file=".env",   # якщо потрібно читати з .env
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
