import datetime
from typing import List, Optional

# MovieDetailResponseSchema

# MovieListResponseSchema

from pydantic import BaseModel

# class MovieBase(BaseModel):
#     name: str
#     date: datetime.date
#     score: float
#     genre: str
#     overview: str
#     crew: str
#     orig_title: str
#     status: str
#     orig_lang: str
#     budget: float
#     revenue: float
#     country: str
#
# class MovieDetailResponseSchema(MovieBase):
#     id: int
#
#     class Config:
#         from_attributes = True
#
# class MovieListResponseSchema(MovieBase):
#
#     class Config:
#         from_attributes = True


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

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    total_pages: int
    total_items: int
    prev_page: Optional[str] = None
    next_page: Optional[str] = None

    class Config:
        from_attributes = True
