import math
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1, description="Page number (must be >= 1)"),
    per_page: int = Query(10, ge=1, le=20, description="Items per page (must be between 1 and 20)"),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page

    count_query = select(func.count()).select_from(MovieModel)
    result = await db.execute(count_query)
    total_items = result.scalar()
    
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = math.ceil(total_items / per_page)

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(query)
    movies = result.scalars().all()

    prev_page = None
    next_page = None
    
    if page > 1:
        prev_page = f"/api/v1/theater/movies/?page={page - 1}&per_page={per_page}"

    if page < total_pages:
        next_page = f"/api/v1/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
    movie_id: int,
    db: AsyncSession = Depends(get_db)
):

    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()
    
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    
    return movie
