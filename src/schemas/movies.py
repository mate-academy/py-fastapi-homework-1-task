from datetime import date

from typing import Optional, List

from pydantic import BaseModel


class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        from_attributes = True


class MovieDetailResponseSchema(BaseSchema):
    id: int
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


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
