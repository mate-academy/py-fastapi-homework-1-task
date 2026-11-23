import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict


class MovieBase(BaseModel):
    name: str = Field(max_length=255)
    date: datetime.date
    score: float = Field(ge=0, le=100)
    genre: str = Field(max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(max_length=255)
    status: str = Field(max_length=50)
    orig_lang: str = Field(max_length=50)
    budget: float
    revenue: float
    country: str = Field(max_length=3)


class MovieDetailResponseSchema(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int = Field(ge=1)
    total_items: int = Field(ge=0)
