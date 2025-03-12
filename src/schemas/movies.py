import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, AnyHttpUrl, computed_field


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: datetime.date
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


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[AnyHttpUrl]
    next_page: Optional[AnyHttpUrl]
    total_pages: int
    total_items: int


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1, description="Page number >= 1")
    per_page: int = Field(10, ge=1, le=20, description="Number of movies per page")

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.per_page
