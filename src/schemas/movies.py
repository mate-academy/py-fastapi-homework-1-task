from pydantic import BaseModel, ConfigDict
from datetime import date
from typing import List, Optional


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
    budget: float  # ← изменено с float на int
    revenue: float  # ← изменено с float на int
    country: str

    model_config: ConfigDict = ConfigDict(from_attributes=True)


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]  # ← имя поля, как требует тест
    prev_page: Optional[str]  # ← строго str, без Optional
    next_page: str  # ← строго str, без Optional
    total_pages: int
    total_items: int

    model_config: ConfigDict = ConfigDict(from_attributes=True)
