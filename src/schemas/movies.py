from pydantic import BaseModel
from typing import List


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: str = None
    score: float = None
    genre: str = None
    overview: str = None
    crew: str = None
    orig_title: str = None
    status: str = None
    orig_lang: str = None
    budget: int = None
    revenue: int = None
    country: str = None

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: [MovieDetailResponseSchema]
    prev_page: int
    next_page: int
    total_pages: int
    total_items: int
