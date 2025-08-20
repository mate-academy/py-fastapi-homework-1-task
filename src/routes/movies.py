from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieSchema

router = APIRouter()

@router.get("/movies", response_model=List[MovieSchema])
async def list_movies(skip: int = 0, limit: int = Query(10, le=100), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).offset(skip).limit(limit))
    movies = result.scalars().all()
    return movies

@router.get("/movies/{movie_id}", response_model=MovieSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
