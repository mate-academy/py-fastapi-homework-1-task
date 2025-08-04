from datetime import date

from pydantic import BaseModel
from decimal import Decimal
from typing import List, Optional


class MovieRead(BaseModel):
    id: int
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: Decimal
    revenue: float
    country: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieRead]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int


class MovieDetailResponseSchema(MovieRead):
    pass
