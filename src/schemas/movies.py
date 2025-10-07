from typing import List, Optional
from datetime import date
from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str

    class Config:
        orm_mode = True
        json_encoders = {
            date: lambda v: v.isoformat(),
        }


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
