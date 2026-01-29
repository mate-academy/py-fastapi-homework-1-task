import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class MovieBase(BaseModel):
    id: int
    name: str = Field(max_length=255)
    date: Optional[datetime.date] = None
    score: float
    genre: str = Field(max_length=255)
    overview: Optional[str] = None
    crew: Optional[str] = None
    orig_title: str = Field(max_length=255)
    status: str = Field(max_length=50)
    orig_lang: str = Field(max_length=50)
    budget: float
    revenue: float
    country: str = Field(max_length=3)


class MovieDetailResponseSchema(MovieBase):

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int

    model_config = ConfigDict(from_attributes=True)
