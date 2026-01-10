import math

from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import MovieModel


class InvalidValueError(Exception):
    def __init__(self, name, description, type_error):
        self.name = name
        self.description = description
        self.type_error = type_error


def get_page_url(page: int, per_page: int):
    return f"/theater/movies/?page={page}&per_page={per_page}"


async def get_movies(db: AsyncSession, page: int, per_page: int):
    if not 1 <= per_page <= 20:
        raise InvalidValueError(
            name="per_page",
            description="Input should be greater than or equal to 1 "
                        "and less or equal to 20",
            type_error="not_ge or not_le"
        )
    if page < 1:
        raise InvalidValueError(
            name="page",
            description="Input should be greater than or equal to 1",
            type_error="not_ge"
        )
    stmt_select_movies = select(MovieModel).offset((page - 1) * per_page).limit(per_page)
    movies = await db.execute(stmt_select_movies)
    movies = movies.scalars().all()
    if not movies:
        raise HTTPException(detail="No movies found.", status_code=404)
    stmt_count_movies = select(func.count()).select_from(MovieModel)
    total_items = await db.scalar(stmt_count_movies)
    total_pages = math.ceil(total_items / per_page)
    prev_page_url = None
    if page > 1:
        prev_page_url = get_page_url(page=page - 1, per_page=per_page)
    next_page_url = None
    if page + 1 <= total_pages:
        next_page_url = get_page_url(page=page + 1, per_page=per_page)

    return {
        "movies": movies,
        "prev_page": prev_page_url,
        "next_page": next_page_url,
        "total_pages": total_pages,
        "total_items": total_items,
    }


async def get_movie(movie_id: int, db: AsyncSession):
    stmt = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(stmt)
    result = result.scalar()
    return result
