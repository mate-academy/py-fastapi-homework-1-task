from datetime import date as date_type
from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict, field_serializer


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[Any] = None
    score: Optional[float] = None
    genre: Optional[str] = None
    overview: Optional[str] = None
    crew: Optional[str] = None
    orig_title: Optional[str] = None
    status: Optional[str] = None
    orig_lang: Optional[str] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    country: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_serializer('date')
    def serialize_date(self, value: Optional[date_type]) -> Optional[str]:
        if value is None:
            return None
        # Handles raw strings safely if already parsed by the driver
        if isinstance(value, str):
            return value
        return value.isoformat()


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
