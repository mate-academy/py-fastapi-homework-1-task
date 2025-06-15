from typing import List, Optional

from pydantic import BaseModel
from datetime import datetime


class MovieBase(BaseModel):
    name: str
    date: datetime
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


class MovieDetailResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d")
        }


class MovieListResponseSchema(BaseModel):
    movies: List[MovieBase]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int

    class Config:
        from_attributes = True
        orm_mode = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d")
        }
