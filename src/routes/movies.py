from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from database import get_db, MovieModel

from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()

@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(page: int = 1, per_page: int = 10, db: AsyncSession = Depends(get_db)):
    offset = (page - 1) * per_page

    result = await db.execute(select(func.count(MovieModel)))
    count_of_movies = result.scalar()   #---> 23
    total_pages = (count_of_movies // per_page) + (1 if count_of_movies % per_page != 0 else 0)

    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    first_movie_result = await db.execute(select(MovieModel))
    first_movie = True if first_movie_result.first() else False
    movies = result.all()

    if page > total_pages or not (1 <= per_page <= 20):
        raise HTTPException(status_code=422, detail="ensure this value is greater than or equal to 1")

    if not first_movie:
        raise HTTPException(status_code=404, detail="No movies found")

    prev_page = None if page == 1 else f"/theater/movies?page={page - 1}&per_page={per_page}"
    next_page = None if page == total_pages else f"/theater/movies?page={page + 1}&per_page={per_page}"

    return JSONResponse(
        status_code=200,
        content={
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": count_of_movies
        }
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id==movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
