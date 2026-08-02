
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from database import get_db, MovieModel


router = APIRouter()


@router.get("/movies/", response_model=schemas.MovieListResponseSchema)
async def get_movies(
    db: AsyncSession = Depends(get_db), page: int = Query(1, ge=1), per_page: int = Query(10, ge=1, le=20)
) -> schemas.MovieListResponseSchema:
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page
    db_movies = await db.scalars(select(MovieModel).offset(offset).limit(per_page))
    movies = db_movies.all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None
    return schemas.MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=schemas.MovieDetailResponseSchema)
async def get_movie_details(movie_id: int, db: AsyncSession = Depends(get_db)) -> schemas.MovieDetailResponseSchema:
    movie = await db.scalar(select(MovieModel).where(MovieModel.id == movie_id))
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return schemas.MovieDetailResponseSchema.model_validate(movie)
