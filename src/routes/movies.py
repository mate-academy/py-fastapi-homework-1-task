from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import (MovieDetailResponseSchema,
                     MovieListResponseSchema)

router = APIRouter(prefix="/movies", tags=["movie"])


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(MovieModel, movie_id)
    if movie is None:
        raise HTTPException(status_code=404,
                            detail="Movie with the given ID was not found.")
    return movie


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(db: AsyncSession = Depends(get_db),
                     page: int = Query(default=1, ge=1),
                     per_page: int = Query(default=10, ge=1, le=20)):

    offset = (page - 1) * per_page
    stmt = select(MovieModel).offset(offset).limit(per_page)
    movies = (await db.execute(stmt)).scalars().all()
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    total_pages = (total_items + per_page - 1) // per_page

    if not movies:
        raise HTTPException(status_code=404,
                            detail="No movies found.")

    prev_page = (
        f"/movies/?page={page - 1}&per_page={per_page}"
        if page > 1 else None
    )
    next_page = (
        f"/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages else None
    )

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )
