from math import ceil
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Path, Request
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    page: Annotated[int, Query(alias="page", ge=1)] = 1,
    per_page: Annotated[int, Query(alias="per_page", ge=1, le=20)] = 10,
    db: AsyncSession = Depends(get_db),
):
    query_all_movies = select(MovieModel)
    query_movies_on_page = query_all_movies.offset((page - 1) * per_page).limit(
        per_page
    )

    movies_coro = await db.scalars(query_movies_on_page)
    movies_list = [movie.as_dict() for movie in movies_coro.all()]

    if not movies_list:
        raise HTTPException(status_code=404, detail="No movies found.")

    all_movies_coro = await db.scalars(query_all_movies)
    total_items = len(all_movies_coro.all())

    response = {"movies": movies_list}

    response["prev_page"] = (
        request.url.path + f"?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    response["next_page"] = request.url.path + f"?page={page + 1}&per_page={per_page}"
    response["total_pages"] = ceil(total_items / per_page)
    response["total_items"] = total_items

    return response


@router.get("/movies/{movie_id:int}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    try:
        movie = await db.get_one(MovieModel, ident=movie_id)
    except NoResultFound:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    movie_dict = movie.as_dict()
    if not isinstance(movie_dict["date"], str):
        movie_dict["date"] = movie_dict["date"].strftime("%Y-%m-%d")

    return movie_dict
