import datetime
from decimal import Decimal
from typing import List, Optional

from pydantic import BaseModel, Field


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
    id: int

    model_config = {
        "from_attributes": True
    }


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
