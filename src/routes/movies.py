import math
from fastapi import APIRouter, Depends, HTTPException, Query, status, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema
router = APIRouter()


@router.get("/movies/")
async def get_movie_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20)
) -> MovieListResponseSchema:
    result = await db.execute(select(func.count(MovieModel.id)))
    total_items = result.scalar()
    if not total_items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")
    total_pages = math.ceil(total_items / per_page)
    offset = (page - 1) * per_page
    stmt = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(stmt)
    movies = result.scalars().all()
    if not movies:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No movies found.")
    base_url = request.url.path
    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None
    )
    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/")
async def get_movie_detail(
    movie_id: int,
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.scalars(stmt)
    movie = result.first()
    if not movie:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Movie with the given ID was not found.")
    return movie
