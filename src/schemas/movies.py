import datetime

from pydantic import BaseModel, ConfigDict

from fastapi import Request


class MovieBase(BaseModel):
    id: int
    name: str
    date: datetime.date
    score: float
    genre: str
    overview: str
    crew: str
    orig_title: str
    status: str
    orig_lang: str
    budget: float
    revenue: float
    country: str

    model_config = ConfigDict(from_attributes=True)


class MovieDetailResponseSchema(MovieBase):
    pass


class MovieListResponseSchema(BaseModel):
    movies: list[MovieDetailResponseSchema]
    prev_page: str | None = None
    next_page: str | None = None
    total_pages: int
    total_items: int


async def get_pagination_urls(request: Request, page: int, per_page: int, total: int):
    base_url = str(request.url.remove_query_params(["page", "per_page"]))

    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if (page * per_page) < total
        else None
    )

    return prev_page, next_page
