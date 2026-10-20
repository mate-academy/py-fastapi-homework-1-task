import datetime

from pydantic import BaseModel, ConfigDict


class MovieDetailResponseSchema(BaseModel):
    """Detailed representation of a movie returned by the API."""

    id: int
    name: str
    date: datetime.date
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

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    """A page of movies together with pagination metadata."""

    movies: list[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int
