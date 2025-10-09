from pydantic import BaseModel
import datetime
from typing import List


class MovieBase(BaseModel):
    name: str
    date: datetime.date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int | float
    country: str


class MovieDetailResponseSchema(MovieBase):
    id: int
    model_config = {"from_attributes": True}


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int
    model_config = {"from_attributes": True}
