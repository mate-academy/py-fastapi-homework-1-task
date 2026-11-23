import math

from fastapi import APIRouter, HTTPException, status, Request

from crud.movies import count_movies, all_movies, get_movie
from dependencies.db import SessionDep
from dependencies.pagination import PaginationHelper
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get(
    "/movies/",
    response_model=MovieListResponseSchema,
    responses={404: {"description": "No movies found"}},
)
async def get_paginated_movies(
    db: SessionDep, pagination: PaginationHelper, request: Request
):
    total_movies = await count_movies(db=db)
    total_pages = math.ceil(total_movies / pagination.per_page)

    movies = await all_movies(
        db=db,
        skip=((pagination.page - 1) * pagination.per_page),
        limit=pagination.per_page,
    )

    if len(movies) == 0:
        raise HTTPException(
            detail="No movies found.", status_code=status.HTTP_404_NOT_FOUND
        )

    prev_page = None
    next_page = None

    if pagination.page - 1 > 0:
        prev_page = (
            str(request.url.path)
            + f"?page={pagination.page - 1}&per_page={pagination.per_page}"
        )

    if pagination.page < total_pages:
        next_page = (
            str(request.url.path)
            + f"?page={pagination.page + 1}&per_page={pagination.per_page}"
        )

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_movies,
    )


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema,
    responses={404: {"description": "Movie with the given ID was not found."}},
)
async def get_movie_detail(db: SessionDep, movie_id: int):
    movie = await get_movie(db=db, movie_id=movie_id)

    if movie is None:
        raise HTTPException(
            detail="Movie with the given ID was not found.",
            status_code=status.HTTP_404_NOT_FOUND,
        )

    return movie
