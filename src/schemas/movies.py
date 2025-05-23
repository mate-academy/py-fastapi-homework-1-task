from pydantic import BaseModel
import datetime
from typing import List


class MovieDetailResponseSchema(BaseModel):
    id: int
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

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]

    total_pages: int
    total_items: int
    next_page: int | None
    prev_page: int | None
