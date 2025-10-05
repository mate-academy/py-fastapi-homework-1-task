from datetime import date
from typing import List, Optional

from pydantic import BaseModel

class MovieDetailResponseSchema(BaseModel):
    id: int
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

    model_config = {
        "from_attributes": True,
    }


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    total_items: int
    total_pages: int
    prev_page: Optional[int]
    next_page: Optional[int]

    model_config = {
    "from_attributes": True,
    }
