from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel, get_db
from schemas.movies import MovieBase, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def read_movies(
    page: int = Query(1, ge=1, description="Page number (>=1)"),
    per_page: int = Query(10, ge=1, le=20, description="Number of movies per page"),
    db: AsyncSession = Depends(get_db),
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    if not total_items:
        raise HTTPException(status_code=404, detail="No movies found.")
    offset = (page - 1) * per_page
    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")
    total_pages = (total_items + per_page - 1) // per_page
    prev_page = (
        f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"/theater/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )
    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieBase)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return MovieBase(**movie.__dict__)
