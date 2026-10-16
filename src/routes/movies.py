from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["movies"])

@router.get("/", response_model=MovieListResponseSchema)
async def get_all_movies(
        page: int = Query(1, ge=1, description="Number of page"),
        per_page: int = Query(10, ge=1, le=20, description="Elements on the page"),
        db: AsyncSession = Depends(get_db),
):

    offset = (page - 1) * per_page
    movies = await db.scalars(select(MovieModel).order_by(MovieModel.id).offset(offset).limit(per_page))
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    prev_page = None
    next_page = None

    if total_items % per_page != 0:
        total_pages = total_items // per_page + 1
    else:
        total_pages = total_items // per_page

    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page=10"
    if total_pages > page:
        next_page = f"/theater/movies/?page={page + 1}&per_page=10"

    return MovieListResponseSchema(
        movies=movies.all(),
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )
