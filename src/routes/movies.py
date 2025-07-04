from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()

@router.get("/movies", response_model=MovieListResponseSchema)
async def list_movies(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db)
):

    total_items = await db.scalar(select(MovieModel).count())
    total_pages = (total_items + limit - 1) // limit if total_items > 0 else 1

    if page > total_pages:
        raise HTTPException(status_code=400, detail="Page number out of range")

    offset = (page - 1) * limit

    result = await db.execute(select(MovieModel).offset(offset).limit(limit))
    movies = result.scalars().all()

    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )

@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).filter_by(id=movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
