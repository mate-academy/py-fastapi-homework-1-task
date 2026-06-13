import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from database import get_db, MovieModel


router = APIRouter()


@router.get("/movies/", response_model=schemas.MovieListResponseSchema)
async def get_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page
    movies = await db.scalars(
        select(MovieModel)
        .offset(offset)
        .limit(per_page)
    )
    movies = movies.all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = None
    next_page = None
    total_items = await db.scalar(
        select(func.count()).select_from(MovieModel)
    )
    total_pages = math.ceil(total_items / per_page)

    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    if page < total_pages:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=schemas.MovieDetailResponseSchema)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db)
):
    movie = await db.scalar(
        select(MovieModel)
        .where(MovieModel.id == movie_id)
    )

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return movie
