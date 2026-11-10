from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import database
import schemas.movies
from database import get_db, MovieModel
from sqlalchemy import func


router = APIRouter()


@router.get("/movies/", response_model=schemas.movies.MovieListResponseSchema)
async def get_all_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20)
):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    if total_items <= 0:
        raise HTTPException(status_code=404, detail="No movies found.")
    result = await db.scalars(
        select(database.models.MovieModel).offset(
            (page - 1) * per_page).limit(per_page)
    )
    total_pages = (total_items + per_page - 1) // per_page

    movies = result.all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    if page <= 1:
        prev_page = None
    else:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    if total_pages <= page:
        next_page = None
    else:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/movies/{movie_id}/", response_model=schemas.movies.MovieDetailResponseSchema)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db)
):
    result = await db.scalars(select(database.models.MovieModel).where(
        database.models.MovieModel.id == movie_id
    ))
    movie = result.one_or_none()
    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
