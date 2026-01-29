import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, ConfigDict


class MovieDetailsResponse(BaseModel):
    id: int
    name: str = Field(max_length=255)
    date: datetime.date
    score: float
    genre: str = Field(max_length=255, examples=["Drama,Action"])
    overview: str = Field(
        examples=["After dominating the boxing world, "
                  "Adonis Creed has been thriving in "
                  "both his career and family life..."]
    )
    crew: str = Field(examples=["Michael B. Jordan, Tessa Thompson"])
    orig_title: str = Field(max_length=255, examples=["Creed III"])
    status: str = Field(max_length=50, examples=["Released"])
    orig_lang: str = Field(max_length=50, examples=["English"])
    budget: float
    revenue: float
    country: str = Field(max_length=3, examples=["UK"])

    model_config = ConfigDict(from_attributes=True)


class MovieListResponse(BaseModel):
    movies: List[MovieDetailsResponse]

    total_items: int = Field(description="Total number of movies")
    total_pages: int = Field(description="Total pages")

    prev_page: Optional[str] = Field(None, examples=["http://api.com/v1/movies?page=1"])
    next_page: Optional[str] = Field(None, examples=["http://api.com/v1/movies?page=3"])

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "movies": [{"id": 1, "name": "Inception", "date": "2010-10-10", "genre": "Drama"}],
                "total_items": 100,
                "total_pages": 10,
                "prev_page": None,
                "next_page": "http://api.com/v1/movies?page=2"
            }
        }
    )
