from math import ceil
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Depends, Query, Request, HTTPException
from sqlalchemy import select, func

from schemas import MovieListResponseSchema, MovieDetailResponseSchema
from src.database import get_db, MovieModel

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))

    if not total_items:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = ceil(total_items / per_page)
    if page > total_pages:
        raise HTTPException(status_code=404,
                            detail="No movies found.")

    offset = (page - 1) * per_page

    result = await db.scalars(
        select(MovieModel)
        .offset(offset)
        .limit(per_page)
    )
    movies = result.all()

    base_url = str(request.url).split("?")[0]

    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}"
        if 1 < page <= total_pages
        else None
    )

    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return MovieListResponseSchema(
        movies=list(movies),
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):
    result = await db.scalar(
        select(MovieModel).where(MovieModel.id == movie_id)
    )

    if not result:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return result
