from pydantic import BaseModel
from datetime import datetime

class MovieBase(BaseModel):
    name: str
    date: datetime
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: int
    country: str

class MovieDetailResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True

class MovieListResponseSchema(MovieBase):
    id: int

    class Config:
        from_attributes = True
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d")
        }