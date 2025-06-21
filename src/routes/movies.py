import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_all_movies(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.name)
        .limit(per_page)
        .offset(offset)
    )
    movies = result.scalars().all()

    if movies:
        total_result = await db.execute(
            select(func.count()).select_from(MovieModel)
        )
        total_items = total_result.scalar()
        total_pages = math.ceil(total_items / per_page)

        url_page = "/theater/movies/?page={}&per_page={}"
        prev_page = url_page.format(page - 1, per_page) if page > 1 else None
        next_page = (
            url_page.format(page + 1, per_page)
            if (page + 1) * per_page < total_items
            else None
        )

        return {
            "movies": movies,
            "total_items": total_items,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page,
        }

    raise HTTPException(status_code=404, detail="No movies found.")


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalars().first()

    if movie:
        return movie

    raise HTTPException(
        status_code=404, detail="Movie with the given ID was not found."
    )
