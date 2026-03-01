import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

import crud
import schemas
from crud import get_single_movie
from database import get_db, MovieModel


router = APIRouter()


# Write your code here
@router.get(
    "/movies/{movie_id}/",
    response_model=schemas.MovieDetailResponseSchema
)
async def get_movie(
        movie_id: int,
        db: Annotated[AsyncSession, Depends(get_db)]
):
    movie = await get_single_movie(db=db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie


@router.get("/movies/", response_model=schemas.MovieListResponseSchema)
async def get_movies(
        db: Annotated[AsyncSession, Depends(get_db)],
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=20)
):

    movies = await crud.get_list_movies(
        db=db,
        per_page=per_page,
        offset=(page - 1) * per_page
    )
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_items = await crud.get_movies_count(db=db)
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")
    total_pages = math.ceil(total_items / per_page)

    prev_page_url = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page_url = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page_url,
        "next_page": next_page_url,
        "total_pages": total_pages,
        "total_items": total_items
    }
