from pydantic import BaseModel, ConfigDict
from datetime import date

from pagination.schemas import BaseListPaginationSchema


class MovieBase(BaseModel):
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


class MovieDetailResponseSchema(MovieBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseListPaginationSchema):
    movies: list[MovieDetailResponseSchema]

