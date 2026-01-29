from typing import Any, Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.models import MovieModel
from database.session import get_db
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(status_code=404,
                            detail="Movie with the given ID was not found.")

    return movie


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    result = await db.execute(
        select(MovieModel).offset(offset).limit(per_page))
    movies: List[MovieModel] = result.scalars().all()

    movies_schema = [
        MovieDetailResponseSchema.model_validate(movie)
        for movie in movies
    ]

    return MovieListResponseSchema(
        movies=movies_schema,
        prev_page=page - 1 if page > 1 else None,
        next_page=page + 1 if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items
    )
