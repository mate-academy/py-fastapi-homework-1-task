from pydantic import BaseModel, ConfigDict, field_validator, ValidationError  # Write your code here
from datetime import date

class BaseMovieSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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


    # @field_validator("date")
    # @classmethod
    # def validate_date(cls, value: date) -> date:
    #     current_year = date.today().year
    #
    #     if value.year > current_year:
    #         raise ValidationError(f"")
    #
    #     return value

class MovieDetailResponseSchema(BaseMovieSchema):

    id: int


class MovieListResponseSchema(BaseModel):

    model_config = ConfigDict(from_attributes=True)

    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int
