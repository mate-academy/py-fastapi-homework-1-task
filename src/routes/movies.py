from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from crud import get_all_movies_paginated, get_movie
from database import get_db
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def retrieve_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    movie = await get_movie(movie_id, db)

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_list_of_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(ge=1, default=1),
        per_page: int = Query(ge=1, le=20, default=10)
):
    response = await get_all_movies_paginated(db, page, per_page)

    if not response["movies"]:
        raise HTTPException(status_code=404, detail="No movies found.")

    return response
