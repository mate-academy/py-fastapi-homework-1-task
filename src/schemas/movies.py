from typing import List, Optional
from datetime import date
from pydantic import BaseModel
from pydantic import BaseModel

try:
    from pydantic import ConfigDict  # v2
except Exception:
    ConfigDict = None

class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Optional[date]
    score: Optional[float]
    genre: Optional[str]
    overview: Optional[str]
    crew: Optional[str]
    orig_title: Optional[str]
    status: Optional[str]
    orig_lang: Optional[str]
    budget: Optional[int]
    revenue: Optional[int]
    country: Optional[str]


    if ConfigDict:
        model_config = ConfigDict(from_attributes=True)

    # v1
    class Config:
        orm_mode = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: str
    next_page: str
    total_pages: int
    total_items: int

    if ConfigDict:
        model_config = ConfigDict(from_attributes=True)


    class Config:
        orm_mode = True