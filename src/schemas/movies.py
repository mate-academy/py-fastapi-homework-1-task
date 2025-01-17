import datetime

from pydantic import BaseModel, ConfigDict


class MovieSchema(BaseModel):
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
    model_config = ConfigDict(from_attributes=True)


class PaginatedMovies(BaseModel):
    movies: list[MovieSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int
