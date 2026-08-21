from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MovieModel
from database.session import get_db
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    # 1. Count database rows
    count_query = select(func.count()).select_from(MovieModel)
    count_result = await db.execute(count_query)
    total_items = count_result.scalar() or 0

    # 2. Check for empty database immediately
    if total_items == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    # 3. Calculate page boundaries
    total_pages = ceil(total_items / per_page)

    # 4. Check if page exceeds the calculated limit
    if page > total_pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    # 5. Retrieve paginated record slice
    offset = (page - 1) * per_page
    movies_query = select(MovieModel).offset(offset).limit(per_page)
    movies_result = await db.execute(movies_query)
    movies = movies_result.scalars().all()

    # 6. Map target pages indicators
    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found.",
        )

    return movie
