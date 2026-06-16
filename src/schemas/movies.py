from pydantic import BaseModel, ConfigDict, Field
from datetime import date
from typing import List, Optional


class MovieBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)
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
    budget: float
    revenue: float
    country: str


class Movie(MovieBase):
    pass


class MovieDetailResponseSchema(MovieBase):
    pass


class MovieListResponseSchema(BaseModel):
    movies: List[Movie]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
