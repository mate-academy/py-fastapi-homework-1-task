from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema
)

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db)
) -> dict:
    offset = (page - 1) * per_page
    query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(query)
    movie_list = result.scalars().all()
    total_movies = len(movie_list)
    total_pages = total_movies // per_page

    if not total_movies:
        raise HTTPException(
            detail="No movies found.",
            status_code=404
        )

    return MovieListResponseSchema(
        movies=[
            MovieDetailResponseSchema(
                id=movie.id,
                name=movie.name,
                date=movie.date,
                score=movie.score,
                genre=movie.genre,
                overview=movie.overview,
                crew=movie.crew,
                orig_title=movie.orig_title,
                status=movie.status,
                orig_lang=movie.orig_lang,
                country=movie.country,
                revenue=movie.revenue,
                budget=movie.budget
            )
            for movie in movie_list
        ],
        prev_page=(
            f"/movies/?page={page}&per_page={per_page}"
            if page > 1 else None
        ),
        next_page=(
            f"/movies/?page={page}&per_page={per_page}"
            if page < total_pages else None
        ),
        total_pages=total_pages,
        total_items=total_movies
    ).model_dump()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(
    movie_id: int,
    db: AsyncSession = Depends(get_db)
) -> MovieModel:
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            detail="Movie with the given ID was not found.",
            status_code=404,
        )

    return movie
