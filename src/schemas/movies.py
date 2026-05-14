import datetime
from typing import List, Annotated, Optional

from pydantic import BaseModel, AfterValidator, ConfigDict


def between_0_and_180(value: float) -> float:
    if not 0 <= value <= 180:
        raise ValueError(f"{value} must be between 0 and 180")
    return value


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: Annotated[float, AfterValidator(between_0_and_180)]
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


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
