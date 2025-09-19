from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies")


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1, description="Page number (must be >= 1)"),
        per_page: int = Query(10, ge=1, le=20, description="Number of movies per page (1-20)"),
        db: AsyncSession = Depends(get_db)
):
    """
    Get a paginated list of movies.

    Args:
        page: Page number (default: 1, minimum: 1)
        per_page: Number of movies per page (default: 10, range: 1-20)
        db: Database session

    Returns:
        MovieListResponseSchema: Paginated list of movies with metadata
    """
    # Calculate offset for pagination
    offset = (page - 1) * per_page

    # Get total count of movies
    total_count_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_count_result.scalar()

    # If no movies found, return 404
    if total_items == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")

    # Calculate total pages
    total_pages = (total_items + per_page - 1) // per_page

    # Check if requested page exceeds available pages
    if page > total_pages:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")

    # Get movies for the current page
    movies_result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
    )
    movies = movies_result.scalars().all()

    # Convert to response schema
    movie_schemas = [
        MovieDetailResponseSchema(
            id=movie.id,
            name=movie.name,
            date=movie.date,
            score=movie.score,
            genre=movie.genre,
            overview=movie.overview,
            crew=movie.crew,
            orig_title=movie.orig_title,
            status=movie.status,
            orig_lang=movie.orig_lang,
            budget=float(movie.budget),
            revenue=float(movie.revenue),
            country=movie.country
        )
        for movie in movies
    ]

    # Generate pagination links
    base_url = "/theater/movies/"
    prev_page = None
    next_page = None

    if page > 1:
        prev_page = f"{base_url}?page={page - 1}&per_page={per_page}"

    if page < total_pages:
        next_page = f"{base_url}?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movie_schemas,
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
    Get a movie by its ID.

    Args:
        movie_id: The ID of the movie to fetch
        db: Database session

    Returns:
        MovieDetailResponseSchema: Movie details
    """
    # Get movie by ID
    movie = await db.get(MovieModel, movie_id)

    if movie is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema(
        id=movie.id,
        name=movie.name,
        date=movie.date,
        score=movie.score,
        genre=movie.genre,
        overview=movie.overview,
        crew=movie.crew,
        orig_title=movie.orig_title,
        status=movie.status,
        orig_lang=movie.orig_lang,
        budget=float(movie.budget),
        revenue=float(movie.revenue),
        country=movie.country
    )
