from datetime import date
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class MovieDetailResponseSchema(BaseModel):
    """
    Schema for a single movie detail response.
    Contains all fields from the MovieModel.
    """
    model_config = ConfigDict(from_attributes=True)

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
    """
    Schema for paginated list of movies.
    Contains list of movies and pagination metadata.
    """
    movies: list[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int = Field(ge=0)
    total_items: int = Field(ge=0)
