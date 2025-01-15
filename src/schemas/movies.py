import datetime

from pydantic import BaseModel
from typing import Optional


class MovieBase(BaseModel):
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


class MovieDetail(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MovieList(BaseModel):
    movies: list[MovieDetail]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
