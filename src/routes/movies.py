from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, MovieModel
from src.schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_with_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie


async def get_obj_count(db: AsyncSession = Depends(get_db)):
    stmt = select(func.count()).select_from(MovieModel)
    result = await db.execute(stmt)
    total_items = result.scalar_one()
    return total_items


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    db: AsyncSession = Depends(get_db),
    page: int = Query(default=1, ge=1),
    per_page: int = Query(10, ge=1, le=100)
):
    stmt = select(MovieModel).offset((page - 1) * per_page).limit(per_page)
    result = await db.execute(stmt)
    movies = result.scalars().all()

    total_items = await get_obj_count(db)

    base_url = str(request.url.path)
    total_pages = (total_items + per_page - 1) // per_page
    prev_page = None
    next_page = None

    if page > 1:
        prev_page = f"{base_url}?page={page - 1}&per_page={per_page}"
    if page < total_pages:
        next_page = f"{base_url}?page={page + 1}&per_page={per_page}"

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }
