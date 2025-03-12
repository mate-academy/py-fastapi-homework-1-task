from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel


async def get_movie(
        movie_id: int,
        db: AsyncSession
):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    return movie


async def get_all_movies_paginated(
        db: AsyncSession,
        page: int,
        per_page: int
):
    offset = (page - 1) * per_page

    result = await db.execute(select(MovieModel))
    all_movies = result.scalars().all()

    movies = all_movies[offset:offset + per_page]
    total_items = len(all_movies)
    total_pages = total_items // per_page + (
        1 if total_items % per_page != 0 else 0
    )

    if page <= 1:
        prev_page = None
    else:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    if page >= total_pages:
        next_page = None
    else:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_items": total_items,
        "total_pages": total_pages
    }
