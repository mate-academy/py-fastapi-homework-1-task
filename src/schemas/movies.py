import datetime
from pydantic import Field
from typing import List, Optional

from pydantic import BaseModel


class MovieBase(BaseModel):
    title: str
    genre: str
    price: float


class MovieCreate(MovieBase):
    pass


class MovieRead(BaseModel):
    id: int
    name: str
    genre: str
    score: float

    class Config:
        from_attributes = True


class MovieDetailResponseSchema(BaseModel):
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


class MovieListResponseSchema(BaseModel):
    movies: List[MovieRead]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
