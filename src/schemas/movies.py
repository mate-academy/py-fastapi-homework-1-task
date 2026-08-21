from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[str] = None
    score: Optional[float] = None
    genre: Optional[str] = None

    # Pydantic v2 configuration to seamlessly map SQLAlchemy ORM models
    model_config = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[int] = None
    next_page: Optional[int] = None
    total_pages: int
    total_items: int
