from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel


async def get_movies(
        db: AsyncSession,
        skip: int,
        limit: int,

):
    result = await db.scalars(select(MovieModel).offset(skip).limit(limit))

    return list(result.all())


async def get_movie(
        db: AsyncSession,
        movie_id: int
):
    result = await db.scalars(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    return result.one_or_none()


async def count_items(db: AsyncSession):
    return await db.scalar(select(func.count(MovieModel.id)))
