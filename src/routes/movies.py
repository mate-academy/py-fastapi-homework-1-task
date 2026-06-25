from typing import Annotated
import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


AsyncDatabase = Annotated[AsyncSession, Depends(get_db)]
PageQuery = Annotated[int, Query(ge=1)]
PerPageQuery = Annotated[int, Query(ge=1, le=20)]


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    db: AsyncDatabase, page: PageQuery = 1, per_page: PerPageQuery = 10
):
    stmt = select(func.count()).select_from(MovieModel)
    total_items = await db.scalar(stmt)
    total_pages = math.ceil(total_items / per_page)

    offset = (page - 1) * per_page
    stmt = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(stmt)
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    base_url = "/theater/movies/"
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(db: AsyncDatabase, movie_id: int):
    stmt = select(MovieModel).where(MovieModel.id == movie_id)

    result = await db.execute(stmt)
    db_movie = result.scalar_one_or_none()

    if db_movie is None:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return db_movie
