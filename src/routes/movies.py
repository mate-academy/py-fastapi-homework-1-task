from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func, ColumnElement
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

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
    page_movies = movies.all()

    if not page_movies:
        raise HTTPException(404, "No movies found.")
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
        movies=page_movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/", status_code=200, response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.scalar(select(MovieModel).where(MovieModel.id == movie_id))
    if result is None:
        raise HTTPException(404, "Movie with the given ID was not found.")
    return result
