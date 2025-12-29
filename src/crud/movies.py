from fastapi import Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from database.models import MovieModel


async def get_all_movies(
        db: AsyncSession = Depends(get_db),
        page: int = 1,
        per_page: int = 10
):

    offset = (page - 1) * per_page

    total_stmt = select(func.count()).select_from(MovieModel)
    result = await db.execute(total_stmt)
    total_items = result.scalar()

    stmt = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(stmt)
    movies = result.scalars().all()

    total_pages = (total_items + per_page - 1) // per_page

    return {
        "movies": [] if movies is None else movies,
        "prev_page": f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "next_page": f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None,
        "total_pages": total_pages,
        "total_items": total_items
    }


async def get_single_movie_by_id(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):

    stmt = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(stmt)
    movie = result.scalar_one_or_none()

    return movie
