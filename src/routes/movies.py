import math

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import MovieModel as Film
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema
from database import get_db

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema, name="get_movies")
async def get_movies(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    total_items = await db.scalar(select(func.count()).select_from(Film))
    total_items = int(total_items or 0)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = math.ceil(total_items / per_page)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    result = await db.scalars(
        select(Film)
        .order_by(Film.id)
        .offset(offset)
        .limit(per_page)
    )
    movies = result.all()

    base_path = request.url.path

    def make_link(p: int) -> str:
        return f"{base_path}?page={p}&per_page={per_page}"

    prev_page = make_link(page - 1) if page > 1 else None
    next_page = make_link(page + 1) if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }

@router.get("/movies/{film_id}/", response_model=MovieDetailResponseSchema)
async def get_film(film_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Film).where(Film.id == film_id))
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return film
