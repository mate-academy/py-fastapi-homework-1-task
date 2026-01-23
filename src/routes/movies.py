from src.database import get_db

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from src.database.models import MovieModel
from src.schemas import movies as schemas

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/", response_model=List[schemas.MovieRead])
async def get_movies(
        skip: int = 0,
        limit: int = 10,
        db: AsyncSession = Depends(get_db)
):
    query = select(MovieModel).offset(skip).limit(limit)
    result = await db.execute(query)
    movie_list = result.scalars().all()
    return movie_list


@router.post("/", response_model=schemas.MovieRead, status_code=status.HTTP_201_CREATED)
async def create_movie(
        movie: schemas.MovieCreate,
        db: AsyncSession = Depends(get_db)
):
    db_movie = MovieModel(**movie.model_dump())
    db.add(db_movie)
    try:
        await db.commit()
        await db.refresh(db_movie)
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already exists or data is invalid"
        )
    return db_movie


@router.get("/{movie_id}", response_model=schemas.MovieRead)
async def get_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found"
        )
    return movie
