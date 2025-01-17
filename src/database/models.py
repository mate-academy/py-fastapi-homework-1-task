import datetime
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from contextlib import contextmanager

from sqlalchemy import String, Float, Text, DECIMAL, UniqueConstraint, Date
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

DATABASE_URL = "sqlite:///example.db"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class Base(DeclarativeBase):
    pass


class MovieModel(Base):
    __tablename__ = "movies"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    genre: Mapped[str] = mapped_column(String(255), nullable=False)
    overview: Mapped[str] = mapped_column(Text, nullable=False)
    crew: Mapped[str] = mapped_column(Text, nullable=False)
    orig_title: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    orig_lang: Mapped[str] = mapped_column(String(50), nullable=False)
    budget: Mapped[float] = mapped_column(DECIMAL(10, 2), nullable=False)
    revenue: Mapped[float] = mapped_column(Float, nullable=False)
    country: Mapped[str] = mapped_column(String(3), nullable=False)

    __table_args__ = (
        UniqueConstraint("name", "date", name="unique_movie_constraint"),
    )

    def __repr__(self):
        return f"<Movie(name='{self.name}', release_date='{self.date}', score={self.score})>"

@contextmanager
def get_db_contextmanager(self):
    """
    Context manager for database sessions.
    Automatically handles session commit/rollback and closing.
    """
    session = Session()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
