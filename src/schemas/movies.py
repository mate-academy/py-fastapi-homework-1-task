from typing import List, Optional

from pydantic import BaseModel, ConfigDict
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
