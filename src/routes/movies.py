from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from database.models import MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from database import get_db

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movies(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie


@router.get("/movies/", response_model=MovieListResponseSchema)
async def list_movies(
    request: Request,
    db: AsyncSession = Depends(get_db),
    per_page: int = Query(10, ge=1, le=100),
    page: int = Query(1, ge=1),
):
    total_items_query = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_items_query.scalar()
    total_pages = (total_items + per_page - 1) // per_page

    offset = (page - 1) * per_page
    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    base_url = str(request.url).split("?")[0]

    def make_page_link(page_num: int | None) -> str | None:
        if page_num is None or page_num < 1 or page_num > total_pages:
            return None
        return f"{base_url}?page={page_num}&per_page={per_page}"

    return {
        "total_items": total_items,
        "total_pages": total_pages,
        "current_page": page,
        "prev_page": make_page_link(page - 1),
        "next_page": make_page_link(page + 1),
        "movies": movies,
    }
