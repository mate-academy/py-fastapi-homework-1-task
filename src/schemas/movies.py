from datetime import date
from pydantic import BaseModel, validator
from typing import List, Optional


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
    budget: int
    revenue: float
    country: str

    @validator('revenue', pre=True)
    def round_revenue(cls, v):
        return round(float(v)) if v is not None else 0

    class Config:
        json_encoders = {
            date: lambda v: v.isoformat()
        }


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
