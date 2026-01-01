from __future__ import annotations

from datetime import date

from pydantic import BaseModel, ConfigDict, Field


class MovieOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date: date
    score: int = Field(ge=0, le=100)
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str


class MoviesPageOut(BaseModel):
    movies: list[MovieOut]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
