import math
from typing import List, Optional
from pydantic import BaseModel

class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[str] = None
    score: Optional[float] = None
    genre: Optional[str] = None
    overview: Optional[str] = None
    crew: Optional[str] = None
    orig_title: Optional[str] = None
    status: Optional[str] = None
    orig_lang: Optional[str] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    country: Optional[str] = None

    class Config:
        from_attributes = True

class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int