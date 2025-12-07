import math
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models import MovieModel
from src.database.session import get_db


movie_router = APIRouter()

@movie_router.get("/movies/", response_model=List[MovieModel])
async def get_all_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page
    total_items = await db.scalar(select(func.count())
                                  .select_from(MovieModel))
    if not total_items:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = await db.execute(select(MovieModel)
                              .offset(offset)
                              .limit(per_page))
    movies = movies.all()

    total_pages = math.ceil(len(total_items) / per_page)
    prev_page = (
        f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages else None
    )
    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@movie_router.get("/movies/{movie_id}", response_model=MovieModel)
async def get_one_movie(db: AsyncSession, movie_id: int):
    movie = await db.scalar(select(MovieModel)
                            .where(MovieModel.id == movie_id))
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie
