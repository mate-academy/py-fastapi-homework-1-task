from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from math import ceil
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()
DbDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        db: DbDep,
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=20)
) -> MovieListResponseSchema:
    offset = (page * per_page) - per_page
    stmt = select(MovieModel).order_by(MovieModel.id).offset(offset).limit(per_page)
    result = await db.scalars(stmt)
    movies = list(result.all())
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_stmt = select(func.count(MovieModel.id))
    total_movies = await db.scalar(total_stmt)
    pages = max(1, ceil(total_movies / per_page))

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    if page == 1:
        prev_page = None

    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"
    if page >= pages:
        next_page = None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=pages,
        total_items=total_movies,
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(db: DbDep, movie_id: int) -> MovieModel:
    movie = await db.get(MovieModel, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
