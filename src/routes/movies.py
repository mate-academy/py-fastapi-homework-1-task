from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

# Absolute imports based on your exact project file hierarchy
from src.database.models import MovieModel
from src.database.session import get_db
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    # 1. Asynchronously count the aggregate total of items
    count_query = select(func.count()).select_from(MovieModel)
    count_result = await db.execute(count_query)
    total_items = count_result.scalar() or 0

    # 2. Compute total page count
    total_pages = ceil(total_items / per_page) if total_items > 0 else 1

    # 3. Fetch paginated slice of movies via offset/limit
    offset = (page - 1) * per_page
    movies_query = select(MovieModel).offset(offset).limit(per_page)
    movies_result = await db.execute(movies_query)
    movies = movies_result.scalars().all()

    # 4. Determine surrounding page indices
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    # Asynchronously locate movie record matching the given primary key
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_or_none()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie not found",
        )

    return movie
