from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


# Write your code here
@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page
    stmt = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(stmt)
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_movies = await db.scalar(select(func.count(MovieModel.id)))
    total_pages = (total_movies + per_page - 1) // per_page
    if not total_movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return {
        "movies": movies,
        "prev_page": (
            f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
        ),
        "next_page": (
            f"/movies/?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        ),
        "total_pages": total_pages,
        "total_items": total_movies,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
