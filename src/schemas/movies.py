# Write your code here
from datetime import datetime
from typing import TypeVar, Generic, List, Optional

from pydantic import BaseModel, conint, GenericModel

T = TypeVar("T")


class PageParams(BaseModel):
    page: conint(ge=1) = 1
    per_page: conint(ge=1, le=20) = 10


class PagedResponseSchema(GenericModel, Generic[T]):
    total: int
    page: int
    size: int
    results: List[T]


class MovieDetailBase(BaseModel):
    name: str
    date: datetime.date


class MovieDetailResponseSchema(MovieDetailBase):
    id: int

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int

