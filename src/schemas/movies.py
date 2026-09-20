from typing import List, Optional
from datetime import date
from pydantic import BaseModel, ConfigDict, Field


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: float
    genre: Optional[str] = None
    overview: Optional[str] = None
    crew: Optional[str] = None
    orig_title: Optional[str] = None
    status: Optional[str] = None
    orig_lang: Optional[str] = None
    budget: float
    revenue: float
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
