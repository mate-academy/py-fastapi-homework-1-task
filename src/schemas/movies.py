import datetime

from pydantic import BaseModel
from typing import List, Optional


class MovieBaseSchema(BaseModel):
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


class MovieDetailResponseSchema(MovieBaseSchema):
    id: int

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
