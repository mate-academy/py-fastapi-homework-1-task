from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from typing import Optional

from database.session import get_db
from database.models import MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1, description="Page number (must be >= 1)"),
        per_page: int = Query(10, ge=1, le=20, description="Items per page (1-20)"),
        db: AsyncSession = Depends(get_db)
):
    """
    Get a paginated list of movies.

    Args:
        page: Page number (starting from 1)
        per_page: Number of items per page (max 20)
        db: Database session

    Returns:
        MovieListResponseSchema with paginated movies

    Raises:
        HTTPException 404: If no movies found
    """
    # Calculate offset
    offset = (page - 1) * per_page

    # Get total count
    count_query = select(func.count(MovieModel.id))
    result = await db.execute(count_query)
    total_items = result.scalar()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Calculate total pages
    total_pages = (total_items + per_page - 1) // per_page  # Ceiling division

    # Check if page exists
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Query movies with pagination
    query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(query)
    movies = result.scalars().all()

    # Build pagination links
    base_url = "/theater/movies/"
    prev_page = None
    next_page = None

    if page > 1:
        prev_page = f"{base_url}?page={page - 1}&per_page={per_page}"

    if page < total_pages:
        next_page = f"{base_url}?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=[MovieDetailResponseSchema.model_validate(movie) for movie in movies],
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a specific movie.

    Args:
        movie_id: ID of the movie to fetch
        db: Database session

    Returns:
        MovieDetailResponseSchema with movie details

    Raises:
        HTTPException 404: If movie not found
    """
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return MovieDetailResponseSchema.model_validate(movie)
