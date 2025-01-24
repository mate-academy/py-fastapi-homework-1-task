from datetime import datetime

from pydantic import BaseModel


class MovieBase(BaseModel):
    id: int
    name: str
    date: datetime
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    orig_lang: str
    budget: int
    revenue: int
    country: str


class MovieListResponseSchema(BaseModel):
    id: int
    name: str


class MovieDetailResponseSchema(MovieBase):
    pass
