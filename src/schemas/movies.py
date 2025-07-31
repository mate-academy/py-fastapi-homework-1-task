from typing import Optional, List
from pydantic import BaseModel, field_validator
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[str]
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: Optional[int]
    revenue: Optional[int]
    country: str

    @field_validator('date', mode='before')
    def date_to_str(cls, v):
        if isinstance(v, date):
            return v.isoformat()
        return v

    @field_validator('revenue', 'budget', mode='before')
    def float_to_int(cls, v):
        if isinstance(v, float):
            return int(v)
        return v

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
