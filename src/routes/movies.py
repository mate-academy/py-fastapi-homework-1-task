from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema,
)


router = APIRouter()


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page

    query = (
        select(MovieModel)
        .offset(offset)
        .limit(per_page)
    )

    result = await db.execute(query)
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found.",
        )

    count_query = select(func.count()).select_from(MovieModel)
    count_result = await db.execute(count_query)
    total_items = count_result.scalar_one()

    total_pages = (total_items + per_page - 1) // per_page

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


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found.",
        )

    return movie

