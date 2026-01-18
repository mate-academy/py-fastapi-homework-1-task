from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, MovieModel
from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter(prefix="/movies")


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        session: AsyncSession = Depends(get_db)):

    total_items = await session.scalar(select(func.count()).select_from(MovieModel))
    total_pages = max(ceil(total_items / per_page), 1)

    result = await session.execute(
        select(MovieModel)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies_data = [MovieDetailResponseSchema.model_validate(m) for m in movies]

    def make_page_url(page_number: int) -> str | None:
        if 1 <= page_number <= total_pages:
            return f"{request.url.include_query_params(page=page_number, per_page=per_page)}"
        return None

    return MovieListResponseSchema(
        movies=movies_data,
        prev_page=make_page_url(page - 1),
        next_page=make_page_url(page + 1),
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalars().first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
