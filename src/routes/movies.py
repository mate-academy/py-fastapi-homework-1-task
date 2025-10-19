from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    # Count total movies
    total_count = await db.scalar(select(func.count()).select_from(MovieModel))
    
    if total_count == 0:
        raise HTTPException(status_code=404, detail="No movies found.")
    
    # Calculate pagination
    total_pages = (total_count + per_page - 1) // per_page
    offset = (page - 1) * per_page
    
    # Check if page exceeds available pages
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")
    
    # Get movies for current page
    result = await db.execute(
        select(MovieModel).offset(offset).limit(per_page)
    )
    movies = result.scalars().all()
    
    # Build pagination URLs
    prev_page = f"/theater/movies/?page={page-1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page+1}&per_page={per_page}" if page < total_pages else None
    
    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_count
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    
    return movie
