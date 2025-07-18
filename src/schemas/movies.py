import datetime

from pydantic import BaseModel


class MovieBase(BaseModel):
    name: str
    date: datetime.date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_language: str
    budget: float
    revenue: float
    country: str
