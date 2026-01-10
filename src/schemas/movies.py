import datetime

from pydantic import BaseModel, Field, ConfigDict


class MovieBaseSchema(BaseModel):
    name: str = Field(max_length=255)
    date: datetime.date
    score: float
    genre: str = Field(max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(max_length=255)
    status: str = Field(max_length=50)
    orig_lang: str = Field(max_length=50)
    budget: float
    revenue: float
    country: str = Field(max_length=3)


class MovieDetailResponseSchema(MovieBaseSchema):
    model_config = ConfigDict(from_attributes=True)
    id: int


class MovieListResponseSchema(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    movies: list[MovieDetailResponseSchema]
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int


class MovieCreateSchema(MovieBaseSchema):
    pass
