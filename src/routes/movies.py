from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import (
    MovieListResponseSchema,
    MovieDetailResponseSchema,
    PaginationParams
)


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    pagination: PaginationParams = Depends(),
    db: AsyncSession = Depends(get_db),
):
    total_items = await db.scalar(select(func.count(MovieModel.id)))

    total_pages = (total_items + pagination.per_page - 1) // pagination.per_page

    if total_items == 0 or pagination.page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    query = select(MovieModel).offset(pagination.offset).limit(pagination.per_page)
    result = await db.execute(query)

    movies = result.scalars().all()

    prev_page = (
        str(request.url.include_query_params(page=pagination.page - 1))
        if pagination.page > 1 else None
    )
    next_page = (
        str(request.url.include_query_params(page=pagination.page + 1))
        if pagination.page < total_pages else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
