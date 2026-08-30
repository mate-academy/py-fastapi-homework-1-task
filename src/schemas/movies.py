from datetime import date
from typing import List, Optional
from pydantic import BaseModel, ConfigDict, Field


class MovieDetailResponseSchema(BaseModel):
    id_: int = Field(alias="id")
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

    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int