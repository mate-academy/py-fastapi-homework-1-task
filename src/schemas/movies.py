from datetime import date
from typing import Annotated

from pydantic import BaseModel, Field


class MovieDetailResponseSchema(BaseModel):
    """Schema for a single movie detail response."""
    id: Annotated[int, Field(description="Unique movie identifier")]
    name: Annotated[str, Field(description="Movie title")]
    date: Annotated[date, Field(description="Release date")]
    score: Annotated[float, Field(description="Movie rating (0-100)")]
    genre: Annotated[str, Field(description="Movie genres (comma-separated)")]
    overview: Annotated[str, Field(description="Movie description")]
    crew: Annotated[str, Field(description="Cast and crew information")]
    orig_title: Annotated[str, Field(description="Original title")]
    status: Annotated[str, Field(description="Release status")]
    orig_lang: Annotated[str, Field(description="Original language")]
    budget: Annotated[float, Field(description="Movie budget")]
    revenue: Annotated[float, Field(description="Movie revenue")]
    country: Annotated[str, Field(description="Country of production")]


class MovieListResponseSchema(BaseModel):
    """Schema for a paginated list of movies response."""
    movies: Annotated[list[MovieDetailResponseSchema], Field(description="List of movies")]
    prev_page: Annotated[str | None, Field(default=None, description="Link to previous page")]
    next_page: Annotated[str | None, Field(default=None, description="Link to next page")]
    total_pages: Annotated[int, Field(description="Total number of pages")]
    total_items: Annotated[int, Field(description="Total number of movies")]
