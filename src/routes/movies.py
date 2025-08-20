from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

# робимо префікс на рівні роутера, щоб шляхи були /movies/... (у main.py вже є /api/v1/theater)
router = APIRouter(prefix="/movies", tags=["movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def list_movies(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    # total items
    total_items = (
        await db.execute(select(func.count()).select_from(MovieModel))
    ).scalar_one()

    offset = (page - 1) * per_page
    result = await db.execute(
        select(MovieModel).order_by(MovieModel.id).offset(offset).limit(per_page)
    )
    items = result.scalars().all()

    # 404 коли порожньо — саме такий текст, як вимагає ТЗ
    if not items:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = ceil(total_items / per_page) if total_items else 0

    # базовий шлях (вже з урахуванням /api/v1/theater/movies/)
    base_path = request.url.path  # напр., /api/v1/theater/movies/
    # формуємо посилання рівно у форматі прикладу
    prev_p = page - 1 if page > 1 else 1
    next_p = page + 1 if total_pages and page < total_pages else (total_pages or 1)
    prev_page = f"{base_path}?page={prev_p}&per_page={per_page}"
    next_page = f"{base_path}?page={next_p}&per_page={per_page}"

    # серіалізуємо через Pydantic-схему
    movies = [
        MovieDetailResponseSchema.model_validate(m)  # v2
        if hasattr(MovieDetailResponseSchema, "model_validate")
        else MovieDetailResponseSchema.from_orm(m)   # v1
        for m in items
    ]

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        # точно співпадає з вимогою рев’ю
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found.",
        )

    return (
        MovieDetailResponseSchema.model_validate(movie)  # v2
        if hasattr(MovieDetailResponseSchema, "model_validate")
        else MovieDetailResponseSchema.from_orm(movie)   # v1
    )