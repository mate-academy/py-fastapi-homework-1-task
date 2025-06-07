from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy import func
from typing import Optional
from database import get_db
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from database.models import MovieModel


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    # Загальна кількість фільмів
    total_items_res = await db.execute(select(func.count(MovieModel.id)))
    total_items = total_items_res.scalar_one()
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages and total_pages != 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page

    query = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = query.scalars().all()

    base_path = "/movies/"
    prev_page = f"{base_path}?page={page-1}&per_page={per_page}" if page > 1 else None
    next_page = (
        f"{base_path}?page={page+1}&per_page={per_page}" if page < total_pages else None
    )

    movies_pydantic = [
        MovieDetailResponseSchema.model_validate(movie) for movie in movies
    ]
    return MovieListResponseSchema(
        movies=movies_pydantic,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = query.scalar_one_or_none()
    if movie is None:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return MovieDetailResponseSchema.model_validate(movie)
