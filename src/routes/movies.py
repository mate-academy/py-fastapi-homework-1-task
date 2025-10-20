import math
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from database.models import MovieModel
from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema,
)
from starlette import status

router = APIRouter(prefix="/movies", tags=["Movies"])

LINK_PREFIX = "/movies/"

def build_link(base: str, page: int, per_page: int) -> str:
    return f"{base}?page={page}&per_page={per_page}"

@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1, description="The page number to fetch"),
    per_page: int = Query(10, ge=1, le=20, description="Number of movies per page"),
    db: AsyncSession = Depends(get_db),
):
    total_items = (
        await db.execute(select(func.count()).select_from(MovieModel))
    ).scalar_one()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    #pagination
    total_pages = math.ceil(total_items / per_page)
    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
    )
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    if page > 1:
        prev_page = build_link(LINK_PREFIX, page - 1, per_page)
    if page < total_pages:
        next_page = build_link(LINK_PREFIX, page + 1, per_page)

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )

@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema, status_code=status.HTTP_200_OK,)
async def get_movie_detail(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    movie = await db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
