import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    movie = await db.scalar(
        select(MovieModel).where(MovieModel.id == movie_id)
    )

    if movie is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )

    return movie


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, le=20, ge=1),
        db: AsyncSession = Depends(get_db)
):
    if page < 1:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": ["query", "per_page"],
                    "msg": "Input should be between 1 and 20",
                    "type": "value_error.number.not_ge"
                }
            ]
        )

    if not (per_page >= 1 and per_page <= 20):
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=[
                {
                    "loc": ["query", "per_page"],
                    "msg": "Input should be between 1 and 20",
                    "type": "value_error.number.not_ge"
                }
            ]
        )

    count_movies = await db.scalar(select(func.count(MovieModel.id)))

    if not count_movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    total_pages = math.ceil(count_movies / per_page)

    if page > total_pages:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    if total_pages >= page + 1:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"
    else:
        next_page = None

    skip = (page - 1) * per_page

    all_movie = (await db.scalars(
        select(MovieModel)
        .offset(skip)
        .limit(per_page)
    )).all()

    return {
        "movies": all_movie,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": count_movies
    }
