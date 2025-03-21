from pydantic import (
    BaseModel,
    conint,
    NonNegativeInt,
)


class PaginationQuerySchema(BaseModel):
    model_config = {"extra": "forbid"}

    page: conint(ge=1) = 1
    per_page: conint(ge=1, le=20) = 10


class PaginationResponseSchema(BaseModel):
    prev_page: str | None
    next_page: str | None
    total_pages: NonNegativeInt
    total_items: NonNegativeInt
