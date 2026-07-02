from pydantic import BaseModel, ConfigDict
from datetime import date


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


class MovieCreate(MovieBase):
    pass


class MovieDetailResponseSchema(MovieBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class MovieListResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    movies: list[MovieDetailResponseSchema]
    prev_page: int | None
    next_page: int | None
    total_pages: int
    total_items: int
