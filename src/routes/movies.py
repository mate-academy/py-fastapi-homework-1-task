from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])


@router.get("/", response_model=MovieListResponseSchema)
async def read_movies(
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))

    if not total_items:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel)
        .offset(offset)
        .limit(per_page)
    )
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = None
    if page > 1:
        prev_page = f"/api/v1/theater/movies/?page={page - 1}&per_page={per_page}"

    next_page = None
    if page < total_pages:
        next_page = f"/api/v1/theater/movies/?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
async def read_movie(movie_id: int,
                     db: AsyncSession = Depends(get_db)
                     ):
    movie = await db.scalar(select(MovieModel).where(MovieModel.id == movie_id))
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
