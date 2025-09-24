from datetime import date
from typing import List, Optional
from pydantic import BaseModel
from pydantic import ConfigDict


class Config:
    model_config = ConfigDict(from_attributes=True)

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
    budget: Optional[float]
    revenue: Optional[float]
    country: str



class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
