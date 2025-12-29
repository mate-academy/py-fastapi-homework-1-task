from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.movies import get_all_movies, get_single_movie_by_id
from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get(
    "/movies/",
    response_model=MovieListResponseSchema
)
async def get_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(
            1,
            ge=1,
            description="Page number"
        ),
        per_page: int = Query(
            10,
            ge=1,
            le=20,
            description="Number of items per page"
        )
):

    movies = await get_all_movies(db = db, page = page, per_page = per_page)

    if len(movies.get("movies")) == 0:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    if page > movies.get("total_pages"):
        raise HTTPException(
            status_code=404,
            detail="Page number out of range."
        )

    return movies


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema
)
async def get_movie_by_id(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):

    movie = await get_single_movie_by_id(db = db, movie_id = movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return movie
