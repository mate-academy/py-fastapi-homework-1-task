from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.settings import get_settings
from src.database.base import Base  # перевір, звідки імпортується Base

settings = get_settings()

DATABASE_URL = f"sqlite:///{settings.PATH_TO_DB}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_sqlite_database():
    """
    Drops and recreates all tables.
    Used for testing environment.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
