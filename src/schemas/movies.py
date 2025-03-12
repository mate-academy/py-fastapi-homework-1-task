from pydantic import BaseModel, condecimal, constr, confloat
from datetime import date


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: date
    score: confloat(ge=0, le=100)
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: constr(max_length=3)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_items: int
    total_pages: int
