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
    budget: float
    revenue: float
    country: str

    model_config = ConfigDict(from_attributes=True)


class MovieDetailResponseSchema(MovieBaseSchema):
    pass


class MovieListResponseSchema(BaseModel):
    movies: List[MovieBaseSchema]
    total_pages: int
    total_items: int
    prev_page: Optional[str]
    next_page: Optional[str]
