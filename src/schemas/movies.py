import datetime
from typing import Optional, List
from pydantic import BaseModel, AnyUrl


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


class MovieDetailResponseSchema(MovieBase):
    pass


class MovieListResponseSchema(BaseModel):
    prev_page: Optional[AnyUrl] = None
    next_page: Optional[AnyUrl] = None
    total_pages: int
    total_items: int
    movies: List[MovieDetailResponseSchema]

    class Config:
        orm_mode = True


class PaginatedMoviesResponse(BaseModel):
    movies: List[MovieListResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
