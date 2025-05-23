from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from schemas import MovieListResponseSchema, MovieDetailResponseSchema
from pydantic import BaseModel, conint

from database import get_db, MovieModel
import math

router = APIRouter()


class PaginationParams(BaseModel):
    page: conint(ge=1) = 1
    per_page: conint(ge=1, le=20) = 10


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        params: PaginationParams = Depends(),
        db: AsyncSession = Depends(get_db)
):
    page = params.page
    per_page = params.per_page
    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel).offset(offset).limit(per_page)
    )
    films = result.scalars().all()

    total_result = await db.execute(select(func.count(MovieModel.id)))
    total = total_result.scalar()

    if not films:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = math.ceil(total / per_page)
    next_page = None if page + 1 > total_pages else page + 1
    prev_page = page - 1 if page - 1 > 0 else None

    return MovieListResponseSchema(
        movies=films,

        total_pages=total_pages,
        total_items=total,

        next_page=next_page,
        prev_page=prev_page
    )


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema
)
async def get_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
