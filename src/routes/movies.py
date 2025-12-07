import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import MovieModel, get_db
from src.schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_all_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page
    total_items = await db.scalar(select(func.count())
                                  .select_from(MovieModel))
    if not total_items:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = await db.execute(select(MovieModel)
                              .offset(offset)
                              .limit(per_page))
    movies = movies.scalars().all()

    total_pages = math.ceil(total_items / per_page)
    prev_page = (
        f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"/theater/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages else None
    )
    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_one_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.execute(select(MovieModel)
                             .where(MovieModel.id == movie_id))
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return movie
