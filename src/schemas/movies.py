from pydantic import BaseModel
from typing import List, Optional
from datetime import date
from decimal import Decimal


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[date]
    score: int
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
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] | None
    next_page: Optional[str] | None
    total_pages: int | None
    total_items: int | None
