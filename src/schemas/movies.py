from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class MovieBase(BaseModel):
    name: str
    date: date
    score: float = Field(ge=0, le=100)
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str = Field(max_length=50)
    budget: float
    revenue: float
    country: str = Field(max_length=3)


class MovieCreate(MovieBase):
    pass


class MovieListResponseSchema(MovieBase):
    total_items: int
    total_pages: int
    prev_page: Optional[str]
    next_page: Optional[str]

    class Config:
        from_attributes = True


class MovieDetailResponseSchema(MovieBase):
    id: int
    overview: str
    crew: str
    orig_title: str
    orig_lang: str
    budget: float
    revenue: float

    class Config:
        from_attributes = True


class MovieUpdate(BaseModel):
    name: Optional[str] = None
    score: Optional[float] = None
    status: Optional[str] = None


class MovieRead(MovieBase):
    id: int

    class Config:
        from_attributes = True
