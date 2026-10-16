from typing import Annotated, List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db
from src.crud.movies import get_movies, count_items, get_movie
from src.schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema
)

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies_list(
        db: Annotated[AsyncSession, Depends(get_db)],
        page: Annotated[
            int, Query(ge=1, description="Items per page")
        ] = 1,
        per_page: Annotated[
            int, Query(ge=1, le=20, description="Items per page")
        ] = 10
):
    skip = (page - 1) * per_page
    movies = await get_movies(db=db, skip=skip, limit=per_page)
    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )
    total_items = await count_items(db=db)
    total_pages = (total_items + per_page - 1) // per_page

    return MovieListResponseSchema(
        movies=movies,
        prev_page=(
            f"/theater/movies/?page={page - 1}&per_page={per_page}"
            if page > 1
            else None
        ),
        next_page=(
            f"/theater/movies/?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        ),
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema
)
async def get_movie_detail(
        db: Annotated[AsyncSession, Depends(get_db)],
        movie_id : int
):
    movie = await get_movie(db=db, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )
    return movie
