from pydantic import BaseModel
from typing import Optional, List
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[date]
    score: Optional[float]
    genre: Optional[str]
    overview: Optional[str]
    crew: Optional[str]
    orig_title: Optional[str]
    status: Optional[str]
    orig_lang: Optional[str]
    budget: Optional[float]
    revenue: Optional[float]
    country: Optional[str]

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
