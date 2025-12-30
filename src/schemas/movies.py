# Write your code here
import datetime
<<<<<<< HEAD
from typing import Optional

from pydantic import BaseModel, AnyUrl


class MovieDetailResponseSchema(BaseModel):
=======
from typing import List, Optional

from pydantic import BaseModel


class MovieBase(BaseModel):
>>>>>>> 2fec9553f095de91dcaebf68b763ea70082776f6
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

<<<<<<< HEAD

class MovieListResponseSchema(BaseModel):
    prev_page: Optional[AnyUrl] = None
    next_page: Optional[AnyUrl] = None
    total_pages: int
    total_items: int
    movies: list[MovieDetailResponseSchema]
=======
    class Config:
        from_attributes = True


class MovieListResponseSchema(MovieBase):
    pass


class MovieDetailResponseSchema(MovieBase):
    pass


class PaginatedMoviesResponse(BaseModel):
    movies: List[MovieListResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
>>>>>>> 2fec9553f095de91dcaebf68b763ea70082776f6
