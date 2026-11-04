import math
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

from starlette import status

import schemas
from database import get_db, MovieModel
from schemas import MovieListResponseSchema

router = APIRouter()

@router.get(
    "/movies/",
    response_model=schemas.movies.MovieListResponseSchema
)
async def movies_get(
        request: Request,
        page: Annotated[int, Query(default=1, ge=1)] = 1,
        per_page: Annotated[int, Query(default=10, ge=1, le=20)] = 10,
        db: AsyncSession = Depends(get_db)
):
    base_endpoint = request.url.path

    count_stmt = select(func.count()).select_from(MovieModel)
    total_items_res = await db.execute(count_stmt)
    total_items = total_items_res.scalar_one()

    total_pages = math.ceil(total_items / per_page) if total_items > 0 else 1

    offset_val = (page - 1) * per_page
    query = select(MovieModel).offset(offset_val).limit(per_page)
    res = await db.execute(query)
    movies = res.scalars().all()

    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    prev_page = (
        f"{base_endpoint}?page={page - 1}&per_page={per_page}"
        if page > 1
        else None
    )

    next_page = (
        f"{base_endpoint}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get(
    "/movies/{movie_id}/",
    response_model=schemas.movies.MovieRead
)
async def movie_get(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    res = await db.execute(query)
    movie = res.scalars().first()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )

    return movie
