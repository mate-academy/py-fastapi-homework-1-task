from datetime import datetime

from pydantic import ConfigDict

from database import Base


class MovieBase(Base):
    name: str
    date: datetime
    score: float
    genre: str
    overview: str
    crew: list[str]
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MovieCreate(MovieBase):
    pass


class MovieRead(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MovieListResponseSchema(Base):
    movies: list[MovieBase]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
