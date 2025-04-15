from datetime import date
from decimal import Decimal

from pydantic import BaseModel, PositiveFloat


class MovieBaseSchema(BaseModel):
    name: str
    date: date
    score: PositiveFloat
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: Decimal
    revenue: float
    country: str


class MovieCreate(MovieBaseSchema):
    pass


class MovieDetailResponseSchema(MovieBaseSchema):
    id: int

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int

    class Config:
        from_attributes = True
