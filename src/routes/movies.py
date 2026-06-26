from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database.session import get_db
from src.database.models import MovieModel
from src.schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema
)


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    total_query = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_query.scalar() or 0
    total_pages = (total_items + per_page - 1) // per_page if total_items > 0 else 0

    if total_items == 0 or (page > total_pages and total_pages > 0):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    offset = (page - 1) * per_page
    query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(query)
    movies = result.scalars().all()

    base_path = "/api/v1/theater/movies/"
    prev = f"{base_path}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_p = f"{base_path}?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "movies": movies,
        "total_pages": total_pages,
        "total_items": total_items,
        "prev_page": prev,
        "next_page": next_p
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalars().first()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )

    return movie
