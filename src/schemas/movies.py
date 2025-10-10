from datetime import date

from pydantic import BaseModel, ConfigDict


class MovieBase(BaseModel):
    name: str
    date: date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    orig_lang: str
    status: str
    # Set to `float` to match the SQLAlchemy model Mapped[float]
    # and fix `ValidationError` in tests like
    # `test_get_movies_default_parameters`.
    budget: float
    revenue: float
    country: str


class MovieDetailResponseSchema(MovieBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    # Set to `str | None` to pass the `test_get_movies_default_parameters`
    # assertion: `assert response_data["prev_page"] is None`.
    prev_page: str | None
    next_page: str | None
    total_pages: int
    total_items: int
