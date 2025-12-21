from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)
):
    total_items_result = await db.execute(select(func.count(MovieModel.id)))
    total_items = total_items_result.scalar()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages and total_pages > 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    result = await db.execute(
        select(MovieModel).offset(offset).limit(per_page)
    )
    movies = result.scalars().all()

    base_url = str(request.url).split('?')[0]

    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}"
        if page > 1 else None
    )
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }
