from datetime import date
from pydantic import BaseModel
from typing import List, Optional


class MovieDetailResponseSchema(BaseModel):
    id: int  # noqa: VNE003
    name: str
    date: date
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

    model_config = {"from_attributes": True}


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
