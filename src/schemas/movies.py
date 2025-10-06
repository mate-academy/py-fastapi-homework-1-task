from __future__ import annotations

import datetime as dt
from typing import Optional, List
from pydantic import BaseModel


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: Optional[str] = None
    date: Optional[dt.date] = None
    score: Optional[float] = None
    genre: Optional[str] = None
    overview: Optional[str] = None
    crew: Optional[str] = None
    orig_title: Optional[str] = None
    status: Optional[str] = None
    orig_lang: Optional[str] = None
    budget: Optional[int] = None
    revenue: Optional[int] = None
    country: Optional[str] = None


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_items: int
