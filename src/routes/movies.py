import math
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from database.models import MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=MovieListResponseSchema, status_code=status.HTTP_200_OK)
async def get_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    # Calculate total item count
    total_items_query = await db.execute(select(func.count(MovieModel.id)))
    total_items = total_items_query.scalar() or 0

    if total_items == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    # Calculate total pages
    total_pages = math.ceil(total_items / per_page)

    # Check if requested page is out of bounds
    if page > total_pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    # Fetch paginated results
    offset = (page - 1) * per_page
    query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(query)
    movies = result.scalars().all()

    # Generate prev and next page URLs matching required format
    prev_page: Optional[str] = (
        f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page: Optional[str] = (
        f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None
    )

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema, status_code=status.HTTP_200_OK)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )

    return movie
