import datetime
from typing import Optional

from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: float | None = None
    genre: str | None = None
    overview: str | None = None
    crew: str | None = None
    orig_title: str | None = None
    status: str | None = None
    orig_lang: str | None = None
    budget: float | None = None
    revenue: float | None = None
    country: str | None = None

    model_config = {"from_attributes": True}


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
