from datetime import date
from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date | None
    score: float | None
    genre: str | None
    overview: str | None
    crew: str | None
    orig_title: str | None
    status: str | None
    orig_lang: str | None
    budget: float | None
    revenue: float | None
    country: str | None

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int
