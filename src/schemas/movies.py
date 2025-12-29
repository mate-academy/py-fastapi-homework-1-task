from typing import Optional

from pydantic import BaseModel
import datetime


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
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
        orm_mode = True


class MovieListResponseSchema(BaseModel):
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
    movies: list[MovieDetailResponseSchema]


    class Config:
        orm_mode = True