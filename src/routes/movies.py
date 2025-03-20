from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()

@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel)
        .offset(offset)
        .limit(per_page)
    )
    movies = result.scalars().all()

    # Count total movies
    total_result = await db.execute(select(MovieModel))
    total_items = len(total_result.scalars().all())
    total_pages = (total_items // per_page) + (1 if total_items % per_page else 0)

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Generate pagination links
    prev_page = f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }

@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
