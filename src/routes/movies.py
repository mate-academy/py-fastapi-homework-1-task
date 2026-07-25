from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db, MovieModel
from database.crud.movies import get_all_movies, get_movie_by_id
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter(prefix="/movies")


@router.get("/")
async def get_movies(
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
) -> MovieListResponseSchema:
    movies, total_items = await get_all_movies(session=db, page=page, per_page=per_page)
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page
    prev_page = (
        f"/theater/movies/?page={page - 1}&per_page={per_page}"
        if page > 1 else None
    )
    next_page = (
        f"/theater/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages else None
    )

    return MovieListResponseSchema(
        movies=[MovieDetailResponseSchema.model_validate(m) for m in movies],
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/")
async def get_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
) -> MovieDetailResponseSchema:
    movie = await get_movie_by_id(session=db, movie_id=movie_id)
    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.model_validate(movie)
