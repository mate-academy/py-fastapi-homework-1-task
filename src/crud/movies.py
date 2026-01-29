from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel


async def get_movies_paginated(db: AsyncSession, page: int, per_page: int):
    total_query = select(func.count()).select_from(MovieModel)
    total_result = await db.execute(total_query)
    total_items = total_result.scalar()

    offset = (page - 1) * per_page
    movie_query = select(MovieModel).offset(offset).limit(per_page)

    result = await db.execute(movie_query)
    movies = result.scalars().all()

    return movies, total_items


async def get_movie_by_id(db: AsyncSession, movie_id: int):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    return result.scalar_one_or_none()
