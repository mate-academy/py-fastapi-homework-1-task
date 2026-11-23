from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from database import MovieModel


async def count_movies(db: AsyncSession) -> int:
    return await db.scalar(select(count(MovieModel.id))) or 0


async def all_movies(db: AsyncSession, skip: int, limit: int) -> Sequence[MovieModel]:
    return (await db.scalars(select(MovieModel).offset(skip).limit(limit))).all()


async def get_movie(db: AsyncSession, movie_id: int) -> MovieModel | None:
    return await db.get(MovieModel, movie_id)
