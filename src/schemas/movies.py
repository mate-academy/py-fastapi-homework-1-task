import datetime
from typing import List, Optional

from pydantic import BaseModel


class MovieBase(BaseModel):
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


class MovieListResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MovieDetailResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MoviePaginatedResponseSchema(BaseModel):
    movies: List[MovieListResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int

    class Config:
        from_attributes = True
