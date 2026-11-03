from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel


async def get_movie_by_id(db_session: AsyncSession, movie_id: int) -> MovieModel | None:
    return await db_session.get(MovieModel, movie_id)


async def get_movies_for_paginated_list(
        db_session: AsyncSession,
        page: int,
        per_page: int,
) -> tuple[list[MovieModel], int]:
    offset = (page - 1) * per_page
    movies = await db_session.scalars(select(MovieModel).offset(offset).limit(per_page))
    count = await db_session.scalar(select(func.count()).select_from(MovieModel))
    return list(movies.all()), count
