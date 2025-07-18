import datetime

from typing import Generic, TypeVar, Optional, List
from pydantic import BaseModel, AnyHttpUrl

M = TypeVar("M")


class MovieBase(BaseModel):
    id: int
    name: str
    date: datetime.date
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


class MovieListResponseSchema(BaseModel, Generic[M]):
    total_items: int
    total_pages: int
    prev_page: Optional[AnyHttpUrl]
    next_page: Optional[AnyHttpUrl]
    movies: List[M]
