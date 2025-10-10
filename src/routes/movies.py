import math

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
):
    offset = (page - 1) * per_page

    query = (
        select(MovieModel, func.count(MovieModel.id).over().label("total_items"))
        .offset(offset)
        .limit(per_page)
    )
    result = await db.execute(query)
    rows = result.all()

    if not rows:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = [row.MovieModel for row in rows]
    total_items = rows[0].total_items
    total_pages = math.ceil(total_items / per_page)

    base_url = "/theater/movies/"

    # `None` is returned to match the schema
    # and pass `test_get_movies_default_parameters`.
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(
    movie_id: int,
    db: AsyncSession = Depends(get_db),
):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
