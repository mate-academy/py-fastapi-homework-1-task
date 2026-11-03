from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_all_movies(
        db: Annotated[AsyncSession, Depends(get_db)],
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20)
) -> MovieListResponseSchema:
    total_items = await db.scalar(select(func.count()).select_from(MovieModel)) or 0
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = await db.scalars(
        select(MovieModel).order_by(MovieModel.id).offset((page - 1) * per_page).limit(per_page)
    )
    movies_list = list(movies.all())
    if not movies_list:
        raise HTTPException(status_code=404, detail="No movies found.")
    total_pages = ceil(total_items / per_page)

    prev_page_url = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page_url = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies_list,
        prev_page=prev_page_url,
        next_page=next_page_url,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
        db: Annotated[AsyncSession, Depends(get_db)],
        movie_id: int,
) -> MovieDetailResponseSchema:
    movie = await db.get(MovieModel, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.model_validate(movie)
