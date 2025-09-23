from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, MovieModel
from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()

@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    # 1. Рахуємо загальну кількість
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))

    # Якщо взагалі немає фільмів → 404
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    # 2. Рахуємо кількість сторінок
    total_pages = (total_items + per_page - 1) // per_page

    # Якщо користувач просить сторінку, якої не існує → 404
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    # 3. Витягуємо потрібний шматок
    result = await db.execute(
        select(MovieModel)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    movies = result.scalars().all()

    # 4. Формуємо дані
    movies_data = [MovieDetailResponseSchema.model_validate(m) for m in movies]

    # 5. prev/next
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies_data,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )

@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema, tags=["movies"])
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema.model_validate(movie)
