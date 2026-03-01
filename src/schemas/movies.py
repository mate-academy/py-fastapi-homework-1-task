# Write your code here
import datetime
from pydantic import BaseModel, ConfigDict


class MovieModelBase(BaseModel):
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


class MoveModelCreate(MovieModelBase):
    pass


class MovieDetailResponseSchema(MovieModelBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):

    movies: list[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int
