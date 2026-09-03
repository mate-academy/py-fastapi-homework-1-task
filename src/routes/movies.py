from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MovieModel
from database.session import get_db
from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema,
)

router = APIRouter(tags=["theater"])


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    count_stmt = select(func.count()).select_from(MovieModel)
    total_items = await db.scalar(count_stmt) or 0

    if total_items == 0:
        raise HTTPException(
            status_code=404,
            detail="No movies found.",
        )

    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages:
        raise HTTPException(
            status_code=404,
            detail="No movies found.",
        )

    offset = (page - 1) * per_page
    movies_stmt = select(MovieModel).offset(offset).limit(per_page)

    result = await db.scalars(movies_stmt)
    movies = result.all()

    prev_page = (
        f"/movies/?page={page - 1}&per_page={per_page}"
        if page > 1
        else None
    )

    next_page = (
        f"/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema,
)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found.",
        )

    return movie
