from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud import get_all_movies, get_movies_count, get_movie_by_id
from database import get_db
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


# Write your code here
@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)):
    movies = await get_all_movies(db=db, start=(page - 1) * per_page, count=per_page)

    if len(movies) == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies_count = await get_movies_count(db=db)
    total_pages = ceil(movies_count / per_page)

    base_url = str(request.url).split("?")[0]

    prev_page = None
    next_page = None

    if page > 1:
        prev_page = f"{base_url}?page={page - 1}&per_page={per_page}"

    if page < total_pages:
        next_page = f"{base_url}?page={page + 1}&per_page={per_page}"

    return {
        "total_pages": total_pages,
        "total_items": movies_count,
        "prev_page": prev_page,
        "next_page": next_page,
        "movies": movies,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(request: Request, movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await get_movie_by_id(db=db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
