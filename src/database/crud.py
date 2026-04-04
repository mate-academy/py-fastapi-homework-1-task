from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import MovieModel


async def get_movie_list_with_limit_offset(db: AsyncSession, offset: int = 0, limit: int = 20):
    stmt = (
        select(
            MovieModel,
            func.count().over().label("total_items")
        )
        .offset(offset)
        .limit(limit)
    )
    return await db.execute(stmt)


async def get_movie_object(db: AsyncSession, movie_id: int):
    return await db.get(MovieModel, movie_id)
