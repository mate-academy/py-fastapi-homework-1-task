import datetime

from pydantic import BaseModel, ConfigDict, field_validator


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
    revenue: int
    country: str
    model_config = ConfigDict(from_attributes=True)

    @field_validator("budget", "revenue", mode="before")
    @classmethod
    def float_to_int(cls, v):
        if isinstance(v, (float, int)):
            return int(v)
        return v


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int
