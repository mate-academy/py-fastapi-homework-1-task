import math
from typing import Annotated
from urllib.parse import urlencode

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel, get_db
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get(
    "/movies/",
    name="movie-list",
    response_model=MovieListResponseSchema,
)
async def get_all_movies(
    request: Request,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
    db: AsyncSession = Depends(get_db),
):
    query = (
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    result = await db.execute(query)
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found.",
        )

    count_query = select(func.count()).select_from(MovieModel)
    count_result = await db.execute(count_query)
    total_items = count_result.scalar_one()

    total_pages = math.ceil(total_items / per_page)
    base_path = request.app.url_path_for("movie-list")

    prev_page = None
    if page > 1:
        prev_query = urlencode(
            {
                "page": page - 1,
                "per_page": per_page,
            }
        )
        prev_page = f"{base_path}?{prev_query}"

    next_page = None
    if page < total_pages:
        next_query = urlencode(
            {
                "page": page + 1,
                "per_page": per_page,
            }
        )
        next_page = f"{base_path}?{next_query}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get(
    "/movies/{movie_id}/",
    name="movie-detail",
    response_model=MovieDetailResponseSchema,
)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found.",
        )

    return movie
