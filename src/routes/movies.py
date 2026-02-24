import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from src.config import get_settings
from src.database import MovieModel, get_db
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

settings = get_settings()

router = APIRouter(prefix="/movies")

BASE_MOVIES_URL = f"{settings.API_VERSION}{settings.THEATER_PREFIX}{router.prefix}"


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies_list(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(
        default=1, ge=1
    ),
    per_page: int = Query(
        default=10, ge=1, le=20
    )
):
    response = {}
    offset = (page - 1) * per_page
    movies_select = (
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
    )
    result = await db.scalars(movies_select)
    movies = result.all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    response["movies"] = movies

    select_total_items = select(func.count(MovieModel.id))
    total_items = await db.scalar(select_total_items)

    total_pages = math.ceil(total_items / per_page)

    prev_page = page - 1

    if prev_page > 0:
        response["prev_page"] = f"{BASE_MOVIES_URL}?page={prev_page}&per_page={per_page}"

    next_page = page + 1

    if next_page <= total_pages:
        response["next_page"] = f"{BASE_MOVIES_URL}?page={next_page}&per_page={per_page}"

    response["total_items"] = total_items

    response["total_pages"] = total_pages

    return response


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(
    movie_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
):
    movie = await db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
