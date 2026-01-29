import datetime

from pydantic import (
    BaseModel,
    Field, ConfigDict,
)


class MovieDetailResponseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(min_length=1, max_length=255)
    date: datetime.date
    score: float
    genre: str = Field(min_length=1, max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(min_length=1, max_length=255)
    status: str = Field(min_length=1, max_length=50)
    orig_lang: str = Field(min_length=1, max_length=50)
    budget: int
    revenue: float
    country: str = Field(min_length=1, max_length=3)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
