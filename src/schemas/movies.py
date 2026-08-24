import datetime

from pydantic import BaseModel, Field, ConfigDict


class MovieBaseSchema(BaseModel):
    name: str = Field(max_length=255)
    date: datetime.date
    score: float = Field(ge=0, le=100)
    genre: str = Field(max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(max_length=255)
    status: str = Field(max_length=50)
    orig_lang: str = Field(max_length=50)
    budget: float = Field(ge=0)
    revenue: float = Field(ge=0)
    country: str = Field(min_length=1, max_length=3)


class MovieResponseBaseSchema(MovieBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class MovieDetailResponseSchema(MovieResponseBaseSchema):
    pass


class MovieListResponseSchema(MovieResponseBaseSchema):
    pass


class MoviesPageSchema(BaseModel):
    movies: list[MovieListResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
