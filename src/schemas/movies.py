from datetime import date
from typing import Any
from pydantic import BaseModel, ConfigDict, PlainSerializer
from typing_extensions import Annotated


CustomDate = Annotated[
    str | date | None,
    PlainSerializer(lambda v: v.isoformat() if isinstance(v, date) else v, return_type=str | None)
]


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: CustomDate = None
    score: float | None = None
    genre: str | None = None
    overview: str | None = None
    crew: str | None = None
    orig_title: str | None = None
    status: str | None = None
    orig_lang: str | None = None
    budget: int | float | None = None
    revenue: int | float | None = None
    country: str | None = None

    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
