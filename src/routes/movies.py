import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from src.schemas import movies


router = APIRouter()


@router.get("/movies/", response_model=movies.MovieListResponseSchema)
async def get_all_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
) -> movies.MovieListResponseSchema:
    total_items_result = await db.execute(select(func.count(MovieModel.id)))
    total_items = total_items_result.scalar_one()
    total_pages = math.ceil(total_items / per_page)

    if page > total_pages or not total_items:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    offset = (page - 1) * per_page

    movies_result = await db.execute(
        select(
            MovieModel
        ).offset(
            offset
        ).limit(per_page)
    )
    movies_items = movies_result.scalars().all()

    return movies.MovieListResponseSchema(
        movies=list(movies_items),
        prev_page=(
            f"/theater/movies/?page={page}&per_page={per_page}"
            if page > 1 else None
        ),
        next_page=(
            f"/theater/movies/?page={page + 1}&per_page={per_page}"
            if page < total_pages else None
        ),
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=movies.MovieDetailResponseSchema)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db)
) -> MovieModel:
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return movie
