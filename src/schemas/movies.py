import datetime

from pydantic import BaseModel, Field
from typing import Optional


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[datetime.date] = None
    score: Optional[float] = None
    genre: Optional[str] = None
    overview: Optional[str] = None
    crew: Optional[str] = None
    orig_title: Optional[str] = None
    status: Optional[str] = None
    orig_lang: Optional[str] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    country: Optional[str] = None

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str] = Field(None, description="URL for the previous page if it exists")
    next_page: Optional[str] = Field(None, description="URL for the next page if it exists")
    total_pages: int
    total_items: int
