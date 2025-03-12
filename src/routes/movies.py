from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema
)
async def get_film(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
) -> MovieDetailResponseSchema:
    movie = await db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie


@router.get(
    "/movies/",
    response_model=MovieListResponseSchema
)
async def get_paginated_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db)
) -> MovieListResponseSchema:

    offset = (page - 1) * per_page

    result = await db.scalars(select(MovieModel).offset(offset).limit(per_page))

    movies = result.all()

    total_movies = await db.scalar(select(func.count()).select_from(MovieModel))

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_movies + per_page - 1) // per_page

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    response = {
        "movies": [
            {
                "id": movie.id,
                "name": movie.name,
                "date": movie.date,
                "score": movie.score,
                "genre": movie.genre,
                "overview": movie.overview,
                "crew": movie.crew,
                "orig_title": movie.orig_title,
                "status": movie.status,
                "orig_lang": movie.orig_lang,
                "budget": movie.budget,
                "revenue": movie.revenue,
                "country": movie.country,
            }
            for movie in movies
        ],
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_movies,
    }
    return response
