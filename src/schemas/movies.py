from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class Movie(BaseModel):
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
    budget: int
    revenue: float
    country: str

    class Config:
        from_attributes = True


class PaginatedMoviesResponse(BaseModel):
    movies: List[Movie]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
