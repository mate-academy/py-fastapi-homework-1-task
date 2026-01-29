from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


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


class MovieDetailResponseSchema(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]

    prev_page: Optional[int]
    next_page: Optional[int]

    total_pages: int
    total_items: int

    model_config = ConfigDict(from_attributes=True)
