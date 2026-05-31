from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

import schemas
from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=schemas.MovieListResponseSchema)
async def movies_list(page: int = Query(default=1, ge=1),
                      per_page: int = Query(default=10, ge=1, le=20),
                      db: AsyncSession = Depends(get_db)):
    count_result = await db.execute(select(func.count(MovieModel.id)))
    total_items = count_result.scalar()

    offset = (page - 1) * per_page
    total_pages = (total_items + per_page - 1) // per_page

    movies = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies_result = movies.scalars().all()
    movies = [MovieDetailResponseSchema.model_validate(m) for m in movies_result]

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    if page == 1:
        prev_page = None
    else:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    if page >= total_pages:
        next_page = None
    else:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(movies=movies, prev_page=prev_page, next_page=next_page,
                                   total_pages=total_pages, total_items=total_items)


@router.get("/movies/{movie_id}/", response_model=schemas.MovieDetailResponseSchema)
async def movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.scalar(select(MovieModel).where(MovieModel.id == movie_id))

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
