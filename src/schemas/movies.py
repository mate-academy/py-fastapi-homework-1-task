from datetime import date

from pydantic import BaseModel, validator
from typing import List, Optional


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: str
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

    class Config:
        from_attributes = True

    @validator("date", pre=True)
    def format_date(cls, v):
        if isinstance(v, date):
            return v.strftime("%Y-%m-%d")
        return v


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int

    class Config:
        from_attributes = True
