from decimal import Decimal

from pydantic import BaseModel, Field
from datetime import date


class MovieDetailResponseSchema(BaseModel):
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


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str
    next_page: str
    total_pages: int
    total_items: int
