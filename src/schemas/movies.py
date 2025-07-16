from datetime import date
from pydantic import BaseModel, Field
from typing import List, Optional


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str = Field(max_length=255)
    date: date
    score: float
    genre: str = Field(max_length=255)
    overview: str
    crew: str
    orig_title: str
    status: str = Field(max_length=50)
    orig_lang: str = Field(max_length=50)
    budget: float
    revenue: float
    country: str = Field(..., max_length=3, min_length=2)

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int

    class Config:
        from_attributes = True
