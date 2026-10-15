from pydantic import BaseModel
from datetime import date


class MoviesBase(BaseModel):
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


class Movies(MoviesBase):
    id: int

    class Config:
        from_attributes = True