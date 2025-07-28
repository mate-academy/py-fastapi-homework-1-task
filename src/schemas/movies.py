from datetime import date
from typing import List, Optional

from pydantic import BaseModel


# Write your code here
class MovieDetailResponseSchema(BaseModel):
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


class MoviesPaginationResponse(BaseModel):
    movies: List[MovieListResponseSchema]
    total_pages: int
    prev_page: Optional[str]
    next_page: Optional[str]
    total_items: int

    class Config:
        from_attributes = True
