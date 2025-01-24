# Write your code here
from datetime import date
from typing import TypeVar, Generic, List, Optional

from pydantic import BaseModel, conint

T = TypeVar("T")


class PageParams(BaseModel):
    page: conint(ge=1) = 1
    per_page: conint(ge=1, le=20) = 10


class PagedResponseSchema(PageParams, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]


class MovieDetailBase(BaseModel):
    id: int
    name: str
    date: date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str


class MovieDetailResponseSchema(MovieDetailBase):

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
