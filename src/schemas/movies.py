from pydantic import BaseModel
from datetime import date


class MovieBase(BaseModel):
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


class MovieListResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True


class MovieDetailResponseSchema(MovieBase):
    class Config:
        from_attributes = True
