from fastapi import APIRouter, Depends, HTTPException, Query

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()
BASE_URL = "/theater/movies/"


def construct_pagination_urls(page: int, per_page: int, total_pages: int) -> tuple[str | None, str | None]:
    """Helper function to generate pagination URLs."""
    prev_page = f"{BASE_URL}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{BASE_URL}?page={page + 1}&per_page={per_page}" if page < total_pages else None
    return prev_page, next_page


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    """Retrieve a paginated list of movies."""
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    if not total_items:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = -(-total_items // per_page)
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = await db.scalars(select(MovieModel).offset((page - 1) * per_page).limit(per_page))
    prev_page, next_page = construct_pagination_urls(page, per_page, total_pages)

    return {
        "movies": movies.all(),
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    """Retrieve a movie by its ID."""
    movie = await db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
