from itertools import count

from pydantic import BaseModel, Field


class MovieBase(BaseModel):
    name: str
    from datetime import date as _date
    date: _date = Field(description='A date')
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


class MovieDetailResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieBase]
