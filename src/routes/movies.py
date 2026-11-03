import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud.movies import get_movie_by_id, get_movies_for_paginated_list
from database import get_db
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie_from_db = await get_movie_by_id(db_session=db, movie_id=movie_id)
    if movie_from_db is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie_from_db


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_paginated_movies_list(
        db_session: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
):
    movies, count = await get_movies_for_paginated_list(db_session=db_session, page=page, per_page=per_page)
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    page_count = math.ceil(count / per_page)
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < page_count else None
    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=page_count,
        total_items=count,
    )
