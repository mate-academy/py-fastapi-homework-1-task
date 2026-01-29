from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    name: str
    date: date | datetime
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MovieDetailResponseSchema(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
