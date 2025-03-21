from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: str
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int | float
    country: str


class MovieListResponseSchema(BaseModel):
    movies: list[dict]
    prev_page: str | None
    next_page: str
    total_pages: int
    total_items: int
