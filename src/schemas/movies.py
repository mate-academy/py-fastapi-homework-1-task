import datetime
from pydantic import BaseModel, BeforeValidator, Field
from typing import List, Union
from typing_extensions import Annotated


def cast_to_int(v):
    if isinstance(v, float):
        return int(v)
    return v


IntCast = Annotated[int, BeforeValidator(cast_to_int)]


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: Union[datetime.date, None] = Field(default=None)
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: IntCast
    country: str

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Union[str, None] = Field(default=None)
    next_page: Union[str, None] = Field(default=None)
    total_pages: int
    total_items: int
