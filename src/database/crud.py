import math
from fastapi import HTTPException

from src.database import models
from src.database.session import AsyncSQLiteSessionLocal
from src.schemas.movies import MoviesPageOut, MovieOut
from sqlalchemy import select, func


async def get_movies_list(page: int, per_page: int, db: AsyncSQLiteSessionLocal) -> list[MoviesPageOut]:
    count_stmt = select(func.count(models.MovieModel.id))
    total_items: int = await db.scalar(count_stmt)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = math.ceil(total_items / per_page)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page

    stmt = select(models.MovieModel).offset(offset).limit(per_page)

    result = await db.execute(stmt)
    movies = result.scalars().all()

    prev_page = (
        f"/movies?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"/movies?page={page + 1}&per_page={per_page}" if page < total_pages else None
    )

    return MoviesPageOut(
        movies=movies,
        total_pages=total_pages,
        prev_page=prev_page,
        next_page=next_page,
        total_items=total_items
    )


async def get_single_movie(db: AsyncSQLiteSessionLocal, movie_id: int) -> MovieOut:
    result = await db.execute(select(models.MovieModel).where(models.MovieModel.id == movie_id))
    return result.scalar_one_or_none()
