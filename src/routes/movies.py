from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from database.models import MovieModel
from database.session import get_db


router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).filter(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie


@router.get("/movies/", response_model=MovieListResponseSchema)
async def list_movies(
    db: AsyncSession = Depends(get_db),
    per_page: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
):
    total_result = await db.execute(select(MovieModel))
    total_items = len(total_result.scalars().all())
    total_pages = (total_items + per_page - 1) // per_page

    offset_value = (page - 1) * per_page
    result = await db.execute(select(MovieModel).offset(offset_value).limit(per_page))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = (
        f"/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None
    )

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )
