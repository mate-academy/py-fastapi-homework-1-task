from datetime import date
from typing import List, Optional
from pydantic import BaseModel


class MovieBase(BaseModel):
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

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies:  Optional[List[MovieBase]] | None
    prev_page: Optional[str] | None
    next_page: Optional[str]  | None
    total_pages: Optional[int]   | None
    total_items: Optional[int]  | None


class MovieDetailResponseSchema(MovieBase):

    class Config:
        from_attributes = True
