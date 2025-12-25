import datetime
from typing import Optional

from pydantic import BaseModel, AnyUrl


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
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


class MovieListResponseSchema(BaseModel):
    prev_page: Optional[AnyUrl] = None
    next_page: Optional[AnyUrl] = None
    total_pages: int
    total_items: int
    movies: list[MovieDetailResponseSchema]
