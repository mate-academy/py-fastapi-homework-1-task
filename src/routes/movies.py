from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


from database import get_db, MovieModel


router = APIRouter(prefix="/movies", tags=["Movies"])

@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
):
    # Підрахунок загальної кількості фільмів
    total_stmt = select(func.count()).select_from(MovieModel)
    total_items = await db.scalar(total_stmt)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Кількість сторінок
    total_pages = (total_items + per_page - 1) // per_page

    # 🟡 Ось тут перевірка на надлишкову сторінку
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Отримання фільмів на конкретній сторінці
    offset = (page - 1) * per_page
    stmt = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(stmt)
    movies = result.scalars().all()

    # Побудова посилань
    base_url = "/theater/movies/"
    prev_page = f"{base_url}?page={max(1, page - 1)}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    stmt = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(stmt)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie


# Write your code here
