import math
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    db: AsyncSession = Depends(get_db),
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
):
    offset_min = page * per_page
    offset_max = (page + 1) * per_page
    result = await db.execute(select(MovieModel))
    all_movies = result.scalars().all()
    paginated_result = all_movies[offset_min:offset_max]
    if not paginated_result:
        raise HTTPException(status_code=404, detail="No movies found.")
    total_pages = math.ceil(len(all_movies) / per_page)
    return {
        "movies": paginated_result,
        "prev_page": request.url.path + f"?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "next_page": request.url.path + f"?page={page + 1}&per_page={per_page}" if page < total_pages else None,
        "total_pages": total_pages,
        "total_items": len(all_movies),
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
