from datetime import date
from typing import List
from pydantic import BaseModel


class MovieBase(BaseModel):
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

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieBase] | None
    prev_page: str | None
    next_page: str | None
    total_pages: int | None
    total_items: int | None


class MovieDetailResponseSchema(MovieBase):

    class Config:
        from_attributes = True
