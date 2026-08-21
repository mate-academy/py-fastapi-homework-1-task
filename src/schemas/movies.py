from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[Any] = None
    score: Optional[float] = None
    genre: Optional[str] = None
    overview: Optional[str] = None  # Added to resolve test fields
    crew: Optional[str] = None      # Added to resolve test fields
    orig_title: Optional[str] = None
    status: Optional[str] = None
    orig_lang: Optional[str] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None  # URL, не int!
    next_page: Optional[str] = None  # URL, не int!
    total_pages: int
    total_items: int
