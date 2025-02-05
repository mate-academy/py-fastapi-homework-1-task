from datetime import date
from typing import List, Optional

from pydantic import BaseModel


class MovieBase(BaseModel):
    name: str
    date: date
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


class Movie(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MovieListResponseSchema(MovieBase):
    id: int


class PageSchema(BaseModel):
    items: List[MovieListResponseSchema]
    total: int
    prev_page: Optional[str] = None
    next_page: Optional[str]


class MovieDetailsResponseSchema(MovieBase):
    id: int
