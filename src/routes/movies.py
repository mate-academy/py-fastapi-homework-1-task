from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema, MoviesPaginationResponse
from starlette import status

router = APIRouter()


@router.get("/movies/", response_model=MoviesPaginationResponse)
async def get_movies(db: AsyncSession = Depends(get_db),
                     page: int = Query(1, ge=1),
                     per_page: int = Query(10, ge=1, le=20),):
    try:
        total_items = await db.scalar(select(func.count()).select_from(MovieModel))
        if total_items == 0:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        print(f"DB Error: {e}")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    offset = (page - 1) * per_page

    if offset >= total_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")

    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()

    prev_page = f"/api/v1/theater/movies?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/api/v1/theater/movies?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MoviesPaginationResponse(
        movies=[MovieListResponseSchema.from_orm(m) for m in movies],
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return MovieDetailResponseSchema.from_orm(movie)
