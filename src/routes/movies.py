from fastapi import APIRouter, Depends, HTTPException
from fastapi_pagination import add_pagination, Page
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination.ext.sqlalchemy import paginate

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=Page[MovieListResponseSchema])
async def get_movies(db: AsyncSession = Depends(get_db)):
    return await paginate(db, select(MovieModel))


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found"
        )
    return movie


add_pagination(router)
