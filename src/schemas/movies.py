from datetime import date
from pydantic import BaseModel


class MovieBase(BaseModel):
    """Base model for movie data with all common fields."""

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

    model_config = {"orm_mode": True}


class MovieDetailResponseSchema(MovieBase):
    """Schema for detailed movie response, includes all fields from MovieBase plus ID."""

    id: int


class MovieListResponseSchema(BaseModel):
    """Schema for paginated list of movies response."""

    movies: list[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int

    model_config = {"orm_mode": True}
