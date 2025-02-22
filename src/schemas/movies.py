from datetime import date
from typing import Optional, List

from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    """Base movie schema with common fields"""

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


class MovieDetailResponseSchema(MovieBase):
    """Schema for detailed movie response"""

    pass


class MovieListResponseSchema(BaseModel):
    """Schema for paginated movie list response"""

    movies: List[MovieBase]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
