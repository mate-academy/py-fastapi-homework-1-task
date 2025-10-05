from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()

@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie


@router.get("/movies", response_model=MovieListResponseSchema)
async def list_movies(page: int = 1,
                      page_size: int = 10,
                      db: AsyncSession = Depends(get_db)):
    count = select(func.count()).select_from(MovieModel)
    count_result = await db.execute(count)
    total_items = count_result.scalar_one()
    total_pages = (total_items + page_size - 1) // page_size
    offset = (page - 1) * page_size

    stmt = (
        select(MovieModel)
        .offset(offset)
        .limit(page_size)
    )
    result = await db.execute(stmt)
    movies_result = result.scalars().all()
    movies = [
        MovieDetailResponseSchema.model_validate(movie) for movie
        in movies_result]

    return MovieListResponseSchema(
        movies=movies,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=page - 1 if page > 1 else None,
        next_page=page + 1 if page < total_pages else None
    )
