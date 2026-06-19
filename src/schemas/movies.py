import datetime
from typing import List, Optional, Union

from pydantic import BaseModel, ConfigDict, field_serializer


class MovieDetailResponseSchema(BaseModel):
    """Full representation of a single movie, matching the MovieModel fields."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date: Union[datetime.date, str]
    score: float
    genre: Optional[str] = None
    overview: Optional[str] = None
    crew: Optional[str] = None
    orig_title: Optional[str] = None
    status: Optional[str] = None
    orig_lang: Optional[str] = None
    budget: Optional[float] = None
    revenue: Optional[float] = None
    country: Optional[str] = None

    @field_serializer("date")
    def serialize_date(self, value: Union[datetime.date, str]) -> str:
        """Always serialize the date as an ISO-8601 string ('YYYY-MM-DD'),
        whether the underlying value came in as a `datetime.date` object
        or already as a string.
        """
        if isinstance(value, datetime.date):
            return value.isoformat()
        return value


class MovieListItemSchema(MovieDetailResponseSchema):
    """Movie representation used inside the paginated list response.

    Identical to the detail schema; kept as a separate name so the list
    item shape can diverge from the detail shape later without breaking
    callers.
    """
    pass


class MovieListResponseSchema(BaseModel):
    """Paginated list of movies."""

    movies: List[MovieListItemSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
