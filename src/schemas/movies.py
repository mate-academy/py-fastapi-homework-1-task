from decimal import Decimal

from pydantic import BaseModel
from typing import List
from datetime import date

class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float | Decimal
    revenue: float | Decimal
    country: str


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str| None = None
    total_pages: int
    total_items: int
