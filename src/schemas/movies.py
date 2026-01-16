from typing import Optional
from datetime import date
from pydantic import BaseModel, field_serializer
from decimal import Decimal


class MovieDetailResponseSchema(BaseModel):
    """Schema for a single movie detail response"""
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

    model_config = {
        "from_attributes": True
    }

    @field_serializer('date')
    def serialize_date(self, dt: date, _info):
        return dt.isoformat()


class MovieListResponseSchema(BaseModel):
    """Schema for paginated list of movies"""
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
