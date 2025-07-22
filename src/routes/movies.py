import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel

from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from sqlalchemy.sql.functions import func

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie


@router.get("/movies/", response_model=MovieListResponseSchema)
async def list_movies(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    stmt_count = select(func.count()).select_from(MovieModel)
    result_count = await db.execute(stmt_count)
    total_items = result_count.scalar_one()

    total_pages = math.ceil(total_items / per_page)

    stmt_movies = select(MovieModel).offset((page - 1) * per_page).limit(per_page)
    result_movies = await db.execute(stmt_movies)
    movies = result_movies.scalars().all()

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }
