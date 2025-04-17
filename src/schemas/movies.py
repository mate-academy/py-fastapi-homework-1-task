import datetime
from typing import List

from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str = None
    price: float = None
    date: datetime.date = None
    score: float = None
    genre: str = None
    overview: str = None
    crew: str = None
    orig_title: str = None
    status: str = None
    orig_lang: str = None
    budget: float = None
    revenue: float = None
    country: str = None

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    total_items: int
    total_pages: int
    current_page: int
    prev_page: str | None
    next_page: str | None
    movies: List[MovieDetailResponseSchema]

    class Config:
        from_attributes = True
