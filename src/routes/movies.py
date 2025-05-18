from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from src.schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema
)

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    if not (items := await db.scalar(select(func.count()).select_from(MovieModel))):
        raise HTTPException(status_code=404, detail="No movies found.")

    if page > (pages := (items + per_page - 1) // per_page):
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    movies = await db.scalars(
        select(MovieModel).offset(offset).limit(per_page)
    )
    movie_list = movies.all()

    prev_page = str(
        request.url_for("get_movies").include_query_params(page=page - 1, per_page=per_page)) if page > 1 else None
    next_page = str(request.url_for("get_movies").include_query_params(page=page + 1,
                                                                       per_page=per_page)) if page < pages else None

    return {
        "movies": list(movie_list),
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": pages,
        "total": items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
) -> MovieDetailResponseSchema:
    movie = await db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
