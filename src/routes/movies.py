import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import (
    MovieListResponseSchema,
    MovieDetailResponseSchema,
)

movie_router = APIRouter(prefix="/movies")


@movie_router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    total_query = select(func.count()).select_from(MovieModel)
    total_items_res = await db.execute(total_query)
    total_items = total_items_res.scalar() or 0

    if total_items == 0:
        raise HTTPException(
            status_code=404, detail="No movies found."
        )

    total_pages = math.ceil(total_items / per_page)

    if page > total_pages and total_pages > 0:
        raise HTTPException(
            status_code=404, detail="No movies found."
        )

    offset = (page - 1) * per_page
    movies_query = (
        select(MovieModel).offset(offset).limit(per_page)
    )
    movies_res = await db.execute(movies_query)
    movies = movies_res.scalars().all()

    base_url = "/api/v1/theater/movies/"
    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}"
        if page > 1
        else None
    )
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@movie_router.get(
    "/{movie_id}/", response_model=MovieDetailResponseSchema
)
async def get_movie_by_id(
    movie_id: int, db: AsyncSession = Depends(get_db)
):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found.",
        )

    return movie
