from datetime import date

from pydantic import (
    BaseModel,
    PositiveInt,
    Field,

    ConfigDict
)

from schemas.paginations import (
    PaginationResponseSchema
)


class MovieDetailResponseSchema(BaseModel):
    id: PositiveInt
    name: str
    date: date
    score: float
    genre: str = Field(..., max_length=255)
    overview: str
    crew: str
    orig_title: str = Field(..., max_length=255)
    status: str = Field(..., max_length=50)
    orig_lang: str = Field(..., max_length=50)
    budget: float = Field(
        ..., ge=0, le=10**10 - 1
    )
    revenue: float
    country: str = Field(..., max_length=3)

    model_config = ConfigDict(
        from_attributes=True
    )


class MovieListResponseSchema(PaginationResponseSchema):
    movies: list[MovieDetailResponseSchema]

    model_config = ConfigDict(
        from_attributes=True
    )
