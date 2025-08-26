from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class MovieBaseSchema(BaseModel):
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
    budget: int
    revenue: int
    country: str

    class Config:
        from_attributes = True


class MovieDetailResponseSchema(MovieBaseSchema):
    pass


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    total_pages: int
    total_items: int
    prev_page: Optional[str]
    next_page: Optional[str]
