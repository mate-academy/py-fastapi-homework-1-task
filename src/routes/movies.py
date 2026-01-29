import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import func

import src.schemas.movies as schemas
from src.database.models import MovieModel
from src.database.session import get_db

router = APIRouter()


@router.get("/movies/", response_model=schemas.MovieListResponseSchema)
async def get_movies(
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
):

    skip = (page - 1) * per_page
    limit = per_page

    movies_list = (
        await db.scalars(
            select(MovieModel).order_by(MovieModel.id).offset(skip).limit(limit)
        )
    ).all()

    total_items = (await db.scalars(select(func.count()).select_from(MovieModel))).one()
    total_pages = math.ceil((total_items + per_page - 1) // per_page)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    if page == 1:
        prev_page = None
    else:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    if page == total_pages:
        next_page = None
    else:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies_list,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=schemas.MovieDetailResponseSchema)
async def get_single_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = (
        await db.scalars(select(MovieModel).where(MovieModel.id == movie_id))
    ).first()
    if movie is None:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
