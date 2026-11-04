from datetime import date
import typing
import json
from pydantic import ConfigDict, BaseModel, field_validator


class MovieBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


class MovieCreate(MovieBase):
    pass


class MovieDetailResponseSchema(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
