import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

import schemas
from database import get_db, MovieModel


router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=schemas.MovieDetailResponseSchema)
async def detail_info_about_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    obj = await db.get(MovieModel, movie_id)
    if obj is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return obj


@router.get("/movies/", response_model=schemas.MovieListResponseSchema)
async def movie_list_with_pagination(page: int = Query(1, ge=1),
                                     per_page: int = Query(10, le=20, ge=1),
                                     db: AsyncSession = Depends(get_db)):
    count_movies = await db.scalar(select(func.count(MovieModel.id)))

    if not count_movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    total_pages = math.ceil(count_movies / per_page)

    if page > total_pages:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    else:
        prev_page = None

    if total_pages >= page + 1:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"
    else:
        next_page = None

    skip = (page - 1) * per_page

    all_movie = (await db.scalars(select(MovieModel).offset(skip).limit(per_page))).all()

    return {
        "movies": all_movie,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": count_movies
    }
