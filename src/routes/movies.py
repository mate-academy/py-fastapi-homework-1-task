from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema
)


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies_list(
        page: int = Query(default=1, ge=1, description="Page number (must be >= 1)"),
        per_page: int = Query(default=10, ge=1, le=20, description="Items per page (1-20)"),
        db: AsyncSession = Depends(get_db)
):
    """
    Get a paginated list of movies.

    - **page**: Page number to fetch (default: 1, min: 1)
    - **per_page**: Number of movies per page (default: 10, min: 1, max: 20)

    Returns:
    - List of movies with pagination metadata

    Raises:
    - 404: If no movies found
    - 422: If validation fails (invalid page or per_page)
    """

    count_query = select(func.count(MovieModel.id))
    result = await db.execute(count_query)
    total_items = result.scalar_one()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = ceil(total_items / per_page)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page

    movies_query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(movies_query)
    movies = result.scalars().all()

    base_url = "/theater/movies/"
    prev_page = None
    next_page = None

    if page > 1:
        prev_page = f"{base_url}?page={page - 1}&per_page={per_page}"

    if page < total_pages:
        next_page = f"{base_url}?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    """
    Get detailed information about a specific movie by ID.

    - **movie_id**: The ID of the movie to retrieve

    Returns:
    - Detailed movie information

    Raises:
    - 404: If movie with the given ID was not found
    """

    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return movie
