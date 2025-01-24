# Write your code here
from datetime import date
from typing import TypeVar, Generic, List, Optional

from pydantic import BaseModel, conint

T = TypeVar("T")


class PageParams(BaseModel):
    page: conint(ge=1) = 1
    per_page: conint(ge=1, le=20) = 10


class PagedResponseSchema(PageParams, Generic[T]):
    movies: List[T]
    total_pages: int
    total_items: int
    prev_page: Optional[str]
    next_page: Optional[str]

    class Config:
        from_attributes = True


def paginate(page_params: PageParams, query, ResponseSchema: BaseModel) -> PagedResponseSchema[T]:

    paginated_query = query.offset((page_params.page - 1) * page_params.per_page).limit(page_params.per_page).all()

    prev_page = (
        f"/theater/movies/?page={page_params.page - 1}&per_page={page_params.per_page}"
        if page_params.page > 1
        else None
    )

    total_pages = int(round(query.count() / page_params.per_page))

    next_page = (
        f"/theater/movies/?page={page_params.page + 1}&per_page={page_params.per_page}"
        if page_params.page < total_pages
        else None
    )

    return PagedResponseSchema(
        total_items=query.count(),
        total_pages=total_pages,
        movies=[ResponseSchema.from_orm(item) for item in paginated_query],
        prev_page=prev_page,
        next_page=next_page,
    )


class MovieDetailBase(BaseModel):
    id: int
    name: str
    date: date
    score: int
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: int
    revenue: float
    country: str


class MovieDetailResponseSchema(MovieDetailBase):

    class Config:
        from_attributes = True


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]
    prev_page: Optional[str]
    next_page: Optional[str]
    total_pages: int
    total_items: int
