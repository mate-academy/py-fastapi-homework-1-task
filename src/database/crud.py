from typing import List

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import MovieModel


async def get_movies(db: AsyncSession, limit: int = 10, offset: int = 0) -> List[MovieModel]:
    stm = select(MovieModel).limit(limit).offset(offset)

    results = await db.scalars(stm)

    results = list(results.all())

    if len(results) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    return results


async def get_movies_count(db: AsyncSession) -> int:
    stmt = select(func.count()).select_from(MovieModel)
    result = await db.execute(stmt)

    return result.scalar() or 0


async def get_movie_by_id(db: AsyncSession, movie_id: int) -> MovieModel:
    result = await db.get(MovieModel, movie_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )

    return result
