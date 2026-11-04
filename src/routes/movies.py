from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    result = await db.scalar(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return result


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_all_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
):
    offset = (page - 1) * per_page
    total_items = await db.scalar(select(func.count(MovieModel.id)))
    total_pages = (total_items + per_page - 1) // per_page
    result = await db.scalars(
        select(MovieModel).offset(offset).limit(per_page)
    )
    movies = result.all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = None
    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    next_page = None
    if page < total_pages:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )
