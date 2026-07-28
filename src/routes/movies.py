import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema,
    get_pagination_urls,
)

router = APIRouter()

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/movies/", response_model=MovieListResponseSchema)
async def read_all_movies(
    request: Request,
    db: SessionDep,
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")
    total_pages = math.ceil(total_items / per_page)
    if page < 1:
        raise HTTPException(
            status_code=422,
            detail={
                "loc": ["query", "page"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
            },
        )
    if per_page < 1:
        raise HTTPException(
            status_code=422,
            detail={
                "loc": ["query", "per_page"],
                "msg": "ensure this value is greater than or equal to 1",
                "type": "value_error.number.not_ge",
            },
        )
    if per_page > 20:
        raise HTTPException(
            status_code=422,
            detail={
                "loc": ["query", "per_page"],
                "msg": "ensure this value is less than or equal to 20",
                "type": "value_error.number.not_le",
            },
        )
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    stmt = await db.scalars(select(MovieModel).offset(offset).limit(per_page))
    movies = stmt.all()
    if len(movies) == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page, next_page = await get_pagination_urls(
        request=request, per_page=per_page, page=page, total=total_items
    )
    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def read_movie(db: SessionDep, movie_id: int):
    movie = await db.scalar(select(MovieModel).where(MovieModel.id == movie_id))
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
