from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


def validation_error(field: str, msg: str, error_type: str):
    return {
        "loc": ["query", f"{field}"],
        "msg": msg,
        "type": error_type
    }


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1),
        size: int = Query(10, ge=1, le=20, alias="per_page"),
        db: AsyncSession = Depends(get_db)
):
    total_items = await db.scalar(select(func.count(MovieModel.id))) or 0
    total_pages = ceil(total_items / size)
    offset = (page - 1) * size

    movies = list((await db.scalars(select(MovieModel).limit(size).offset(offset))).all())
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return MovieListResponseSchema(
        movies=movies,
        prev_page=f"/theater/movies/?page={page - 1}&per_page={size}" if page > 1 else None,
        next_page=f"/theater/movies/?page={page + 1}&per_page={size}" if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def retrieve_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = (await db.scalar(select(MovieModel).where(MovieModel.id == movie_id)))

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
