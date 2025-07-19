from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from routes.helpers import paginate
from schemas import MovieListResponseSchema, MovieBase

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema[MovieBase])
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MovieModel))
    movie = result.scalar()
    if not movie:
        raise HTTPException(status_code=404, detail="No movies found.")

    return await paginate(db, select(MovieModel), page, per_page)
