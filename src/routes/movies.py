from fastapi import APIRouter, Depends, Request, HTTPException
from fastapi_pagination.ext.sqlalchemy import apaginate
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from pagination import MoviesPage
from schemas import MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/")
async def get_movie_list(
    request: Request,
    db: AsyncSession = Depends(get_db),
) -> MoviesPage:
    result = await apaginate(
        db,
        select(MovieModel),
        additional_data={
            "url": str(request.url),
        },
    )

    if not result.results:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    return result


@router.get("/movies/{movie_id}/")
async def get_movie_by_id(
    movie_id: int, db: AsyncSession = Depends(get_db)
) -> MovieDetailResponseSchema:
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return movie
