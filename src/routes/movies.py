import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from src.database.models import MovieModel
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/")
async def read_movies(page: int = Query(1, ge=1),
                      per_page: int = Query(10, ge=1, le=20),
                      db: AsyncSession = Depends(get_db)):

    offset = (page - 1) * per_page
    stmt = select(MovieModel).order_by(MovieModel.id).offset(offset).limit(per_page)
    total_items_query = select(func.count()).select_from(MovieModel)
    total_items_result = await db.execute(total_items_query)
    total_items = total_items_result.scalar_one_or_none()
    total_pages = math.ceil(total_items / per_page)

    result = await db.execute(stmt)

    movies = result.scalars().all()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    if page > total_pages > 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page,
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
