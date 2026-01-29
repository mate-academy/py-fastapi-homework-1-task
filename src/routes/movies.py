from math import ceil
from typing import List, Annotated
from fastapi import Request

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from crud import movies
import schemas
from database import get_db

router = APIRouter(
    prefix="/movies",
    tags=["movies"]
)


@router.get("/", response_model=List[schemas.movies.MovieListResponse])
async def list_movies(
        page: Annotated[int, Query(ge=1)] = 1,
        per_page: Annotated[int, Query(ge=1, le=20)] = 10,
        db: AsyncSession = Depends(get_db)
):
    movies_, total_items = await movies.get_movies_paginated(db, page, per_page)

    total_pages = ceil(total_items / per_page) if total_items > 0 else 1

    base_url = str(Request.url).split('?')[0]

    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    def create_link(p: int):
        return f"{base_url}?page={p}&per_page={per_page}"

    return {
        "movies": movies_,
        "total_items": total_items,
        "total_pages": total_pages,
        "prev_page": create_link(page - 1) if page > 1 else None,
        "next_page": create_link(page + 1) if page < total_pages else None
    }


@router.get("/{movie_id}/", response_model=schemas.movies.MovieDetailsResponse)
async def get_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    movie_ = await movies.get_movie_by_id(db, movie_id)

    if not movie_:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )

    return movie_
