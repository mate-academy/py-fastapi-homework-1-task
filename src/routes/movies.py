from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.models import MovieModel

from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema,
)

router = APIRouter()


@router.get(
    "/movies/",
    response_model=MovieListResponseSchema,
    status_code=status.HTTP_200_OK
)
async def get_movies(
        db: Annotated[AsyncSession, Depends(get_db)],
        page: Annotated[int, Query(ge=1, description="Page number")] = 1,
        per_page: Annotated[
            int, Query(ge=1, le=20, description="Items per page")] = 10
):
    offset = (page - 1) * per_page
    count_query = select(func.count()).select_from(MovieModel)
    total_items = await db.scalar(count_query)

    if total_items == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(query)
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    total_pages = (total_items + per_page - 1) // per_page

    base_url = "/theater/movies/"
    prev_page_url = None
    if page > 1:
        prev_page_url = f"{base_url}?page={page - 1}&per_page={per_page}"

    next_page_url = None
    if page < total_pages:
        next_page_url = f"{base_url}?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page_url,
        "next_page": next_page_url,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema,
    status_code=status.HTTP_200_OK
)
async def get_movie_by_id(
        movie_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
) -> MovieModel:
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )

    return movie
