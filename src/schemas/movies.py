import datetime

from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: float
    country: str

    class Config:
        orm_mode = True


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str
    next_page: str
    total_pages: int
    total_items: int
