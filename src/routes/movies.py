from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel, get_db
from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema,
)


router = APIRouter(prefix="/movies")


@router.get(
    "/",
    response_model=MovieListResponseSchema,
)
async def get_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
) -> MovieListResponseSchema:
    count_query = select(func.count(MovieModel.id))
    count_result = await db.execute(count_query)
    total_items = count_result.scalar_one()

    offset = (page - 1) * per_page

    movies_query = (
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
    )

    movies_result = await db.execute(movies_query)
    movies = movies_result.scalars().all()

    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found.",
        )

    total_pages = ceil(total_items / per_page)

    prev_page = None
    next_page = None

    if page > 1:
        prev_page = (
            f"/api/v1/theater/movies/"
            f"?page={page - 1}&per_page={per_page}"
        )

    if page < total_pages:
        next_page = (
            f"/api/v1/theater/movies/"
            f"?page={page + 1}&per_page={per_page}"
        )

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get(
    "/{movie_id}/",
    response_model=MovieDetailResponseSchema,
)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
) -> MovieDetailResponseSchema:
    movie_query = select(MovieModel).where(
        MovieModel.id == movie_id
    )

    movie_result = await db.execute(movie_query)
    movie = movie_result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found.",
        )

    return MovieDetailResponseSchema.model_validate(movie)
