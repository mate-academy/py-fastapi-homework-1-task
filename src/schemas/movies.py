import datetime

from pydantic import BaseModel, Field
from sqlalchemy import DECIMAL


class MovieSchema(BaseModel):
    id: int
    name: str = Field(max_length=255)
    date: datetime.date
    score: float = Field()
    genre: str = Field(max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(max_length=255)
    status: str = Field(max_length=50)
    orig_lang: str = Field(max_length=50)
    budget: float
    revenue: float = Field(ge=0)
    country: str = Field(min_length=2, max_length=3)


class MoviesSchema(BaseModel):
    movies: list[MovieSchema]
    prev_page: str | None = Field(max_length=255)
    next_page: str | None = Field(max_length=255)
    total_pages: int
    total_items: int
