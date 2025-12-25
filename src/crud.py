from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select
from sqlalchemy.sql.functions import func

import database


async def get_all_movies(db: AsyncSession, start: int, count: int):
    query = select(database.MovieModel).offset(start).limit(count)
    data = await db.execute(query)
    return data.scalars().all()


async def get_movie_by_id(db: AsyncSession, movie_id: int):
    query = select(database.MovieModel).where(database.MovieModel.id == movie_id)
    data = await db.execute(query)
    return data.scalar_one_or_none()


async def get_movies_count(db: AsyncSession):
    query = select(func.count(database.MovieModel.id))
    result = await db.execute(query)
    return result.scalar_one()
