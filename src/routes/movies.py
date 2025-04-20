from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.movies import PaginatedMoviesResponse, Movie
from database import get_db
from database.models import MovieModel

router = APIRouter()


@router.get("/movies/", response_model=PaginatedMoviesResponse)
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

    return {
        "movies": [Movie.model_validate(movie) for movie in movies],
        "prev_page": (
            f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
        ),
        "next_page": (
            f"/movies/?page={page + 1}&per_page={per_page}"
            if len(movies) == per_page
            else None
        ),
        "total_pages": 1000,
        "total_items": 9999,
    }


@router.get("/movies/{movie_id}/", response_model=Movie)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(stmt)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return Movie.model_validate(movie)
