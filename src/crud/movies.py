from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MovieModel


async def get_movie_list(db: AsyncSession, page: int, per_page: int):
    count = select(func.count()).select_from(MovieModel)
    offset = (page - 1) * per_page

    total_items = await db.scalar(count)

    db_selection = (
        select(MovieModel)
        .offset(offset)
        .limit(per_page)
    )

    query = await db.execute(db_selection)
    movies = query.scalars().all()

    return movies, total_items
