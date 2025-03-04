from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()

@router.get("/movies")
async def get_movies(
        response_model: MovieListResponseSchema = Depends(get_db),
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(1, ge=1, le=20),
):
    total_items = await db.execute(select(MovieModel).count())
    total_pages = (total_items // per_page) + (1 if total_items % per_page else 0)
    offset = (page - 1) * per_page
    if offset > total_items:
        raise HTTPException(status_code=404, detail="Page not found")
    result = await db.execute()
    if result.rowcount == 0:
        raise HTTPException(status_code=404, detail="Page not found")
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None
    movies = await db.execute(
        select(MovieModel).offset((page - 1) * per_page).limit(per_page)
    )
    movies = movies.scalars().all()
    return response_model()
