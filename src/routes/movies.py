import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import movies as crud
from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema
from schemas.movies import MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
    db: AsyncSession = Depends(get_db),
):

    movies = await crud.get_all_movies(db=db, page=page, per_page=per_page)

    count = await crud.get_count_movies(db=db)

    if not movies and count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="No movies found."
        )

    total_pages = math.ceil(count / per_page)

    response = {
        "movies": movies,
        "prev_page": (
            None
            if page == 1
            else f"/theater/movies/?page={page - 1}&per_page={per_page}"
        ),
        "next_page": (
            None
            if page >= total_pages
            else f"/theater/movies/?page={page + 1}&per_page={per_page}"
        ),
        "total_pages": total_pages,
        "total_items": count,
    }
    return response


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await crud.get_movie_by_id(db=db, movie_id=movie_id)
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found.",
        )

    return movie
