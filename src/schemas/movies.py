from datetime import date
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class MovieDetailResponseSchema(BaseModel):
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

    # class Config:
    #     from_attributes = True

    model_config = ConfigDict(from_attributes=True)  # new configuration method


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
