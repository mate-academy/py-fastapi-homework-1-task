from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, between
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.functions import count

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_film(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return film


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, alias="page", ge=1),
    per_page: int = Query(10, alias="per_page", ge=1),
    db: AsyncSession = Depends(get_db),
):
    total_movie = await db.execute(count(MovieModel.id))
    movies = await db.execute(
        select(MovieModel).offset((page - 1) * per_page).limit(per_page)
    )

    return_movies = movies.scalars().all()
    total_movie = total_movie.scalar_one()
    total_pages = max(total_movie // per_page, 1)

    base_url = "/movies"
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None

    if return_movies:
        return {
            "movies": return_movies,
            "total_items": total_movie,
            "total_pages": total_pages,
            "next_page": next_page,
            "prev_page": prev_page,
        }

    raise HTTPException(status_code=404, detail="No movies found.")
