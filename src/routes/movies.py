from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
import math

from database import get_db, MovieModel
from crud import get_all_movies, get_movies_count, get_movie_by_id
from database import get_db
from schemas import MovieListResponseSchema, MovieDetailResponseSchema
from schemas import PaginatedMoviesResponse, MovieDetailResponseSchema



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
=======

@router.get("/movies/", response_model=PaginatedMoviesResponse)
async def get_movies(
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    offset = (page - 1) * per_page

    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()

    total_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_result.scalar()

    prev_page = f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/movies/?page={page + 1}&per_page={per_page}" \
        if offset + len(movies) < total_items else None

    total_pages = math.ceil(total_items / per_page)

    response = {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")
    return response


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalars().first()
>>>>>>> 2fec9553f095de91dcaebf68b763ea70082776f6
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
