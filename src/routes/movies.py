from typing import Annotated
from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_all_movies(
        session: Annotated[AsyncSession, Depends(get_db)],
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
):
    total_items = await session.scalar(select(func.count(MovieModel.id)))
    total_pages = ceil(total_items / per_page)

    movies = (await session.scalars(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )).all()

    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    def link(p: int) -> str:
        return f"/theater/movies/?page={p}&per_page={per_page}"
    return {
        "movies": movies,
        "prev_page": link(page - 1) if page > 1 else None,
        "next_page": link(page + 1) if page < total_pages else None,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(
        session: Annotated[AsyncSession, Depends(get_db)],
        movie_id: int,
):
    movie = await session.scalar(select(MovieModel).where(MovieModel.id == movie_id))
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
