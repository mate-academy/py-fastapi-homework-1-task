from __future__ import annotations

from math import ceil
from urllib.parse import urlparse
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from ..database.models import MovieModel
from ..database.session import get_db
from ..schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])


def _path_only(url: str) -> str:
    """Повертає тільки шлях частини URL (без схеми/хоста/порту)."""
    return urlparse(url).path


@router.get("/", response_model=MovieListResponseSchema)
async def list_movies(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    # total items
    total_items = (await db.execute(select(func.count()).select_from(MovieModel))).scalar_one()
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    # pagination calc
    total_pages = ceil(total_items / per_page)
    offset = (page - 1) * per_page

    # якщо виходимо за межі — 404 як у вимозі
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
    )
    rows = result.scalars().all()

    if not rows:
        # порожня вибірка на валідній сторінці — вважаємо як "не знайдено"
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = [MovieDetailResponseSchema.model_validate(r, from_attributes=True) for r in rows]

    # будуємо prev/next як ШЛЯХ (а не повний URL), як у прикладі
    base_path = _path_only(request.url_for("list_movies"))

    prev_page: Optional[str] = None
    if page > 1:
        prev_page = f"{base_path}?page={page-1}&per_page={per_page}"

    next_page: Optional[str] = None
    if page < total_pages:
        next_page = f"{base_path}?page={page+1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_details(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema.model_validate(movie, from_attributes=True)
