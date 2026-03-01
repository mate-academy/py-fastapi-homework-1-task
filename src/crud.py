from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from database import models


async def get_list_movies(
        db: AsyncSession,
        per_page: int,
        offset: int
) -> list[models.MovieModel]:
    stmt = select(models.MovieModel).offset(offset).limit(per_page)
    result = await db.scalars(stmt)
    return result.all()


async def get_single_movie(
        db: AsyncSession,
        movie_id: int
) -> models.MovieModel | None:
    return await db.scalar(
        select(models.MovieModel).where(models.MovieModel.id == movie_id)
    )


async def get_movies_count(db: AsyncSession) -> int:
    stmt = select(func.count()).select_from(models.MovieModel)
    result = await db.scalar(stmt)
    return result or 0
