import math

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db, crud
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


class PaginationParams:
    def __init__(
        self,
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=20)
    ):
        self.page = page
        self.per_page = per_page
        self.skip = (page - 1) * per_page


@router.get(
    "/movies/",
    response_model=MovieListResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_movies(
    db: AsyncSession = Depends(get_db),
    pagination: PaginationParams = Depends()
):
    total_items = await crud.get_movies_count(db)
    total_pages = math.ceil(total_items / pagination.per_page) if total_items > 0 else 1
    prev_page = None
    next_page = None

    prefix = "/theater/movies/"

    if pagination.page > 1:
        prev_page = f"{prefix}?page={pagination.page - 1}&per_page={pagination.per_page}"

    if pagination.page < total_pages:
        next_page = f"{prefix}?page={pagination.page + 1}&per_page={pagination.per_page}"

    movies = await crud.get_movies(db, limit=pagination.per_page, offset=pagination.skip)

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    return await crud.get_movie_by_id(db, movie_id)
