import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.models import MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=20, description="Items per page"),
    db: AsyncSession = Depends(get_db),
):

    count_query = select(func.count()).select_from(MovieModel)
    total_items_result = await db.execute(count_query)
    total_items = total_items_result.scalar_one()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = math.ceil(total_items / per_page)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    # 3. Витягуємо фільми для поточної сторінки (пагінація через offset / limit)
    offset = (page - 1) * per_page
    stmt = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(stmt)
    movies = result.scalars().all()

    base_path = "/theater/movies/"
    prev_page = (
        f"{base_path}?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"{base_path}?page={page + 1}&per_page={per_page}"
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


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
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

    return movie
