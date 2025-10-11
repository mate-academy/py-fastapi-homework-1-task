from datetime import date

from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    orig_lang: str
    status: str
    budget: float
    revenue: float
    country: str


class MovieDetailResponseSchema(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str
    next_page: str
    total_pages: int
    total_items: int
