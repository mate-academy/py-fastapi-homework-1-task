from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import MovieModel


async def get_all_movies(db: AsyncSession, page: int, per_page: int):
    skip = (page - 1) * per_page

    movies = await db.scalars(select(MovieModel).offset(skip).limit(per_page))
    return movies.all()


async def get_count_movies(db: AsyncSession):
    count = await db.scalar(select(func.count(MovieModel.id)))
    return count


async def get_movie_by_id(db: AsyncSession, movie_id: int):
    movie = await db.scalar(select(MovieModel).where(MovieModel.id == movie_id))
    return movie
