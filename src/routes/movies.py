import math

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movie_list(
    db: Annotated[AsyncSession, Depends(get_db)],
    request: Request,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
):
    count_items = await db.execute(
        select(func.count()).select_from(MovieModel)
    )
    total_items = count_items.scalar() or 0
    total_pages = math.ceil(total_items / per_page)

    if total_items == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )
    if page > total_pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    start_item = per_page * page - per_page
    result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(start_item)
        .limit(per_page)
    )
    movies = result.scalars().all()

    full_url = request.url_for("get_movie_list")
    prev_page = (
        str(full_url.include_query_params(page=page - 1, per_page=per_page))
        if page > 1
        else None
    )
    next_page = (
        str(full_url.include_query_params(page=page + 1, per_page=per_page))
        if (total_pages - page) >= 1
        else None
    )

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_items=total_items,
        total_pages=total_pages,
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
    movie_id: int, db: Annotated[AsyncSession, Depends(get_db)]
):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found.",
        )
    return movie
