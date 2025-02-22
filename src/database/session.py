from contextlib import contextmanager
from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from config import get_settings
from database import Base

settings = get_settings()

DATABASE_URL = f"sqlite:///{settings.PATH_TO_DB}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

connection = engine.connect()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=connection)

Base.metadata.create_all(bind=engine)


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@contextmanager
def get_db_contextmanager() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def reset_sqlite_database():
    with connection.begin():
        Base.metadata.drop_all(bind=connection)
        Base.metadata.create_all(bind=connection)
