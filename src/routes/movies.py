from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


def movie_to_dict(movie: MovieModel) -> dict:
    return {
        "id": movie.id,
        "name": movie.name,
        "date": str(movie.date),
        "score": movie.score,
        "genre": movie.genre,
        "overview": movie.overview,
        "crew": movie.crew,
        "orig_title": movie.orig_title,
        "status": movie.status,
        "orig_lang": movie.orig_lang,
        "budget": float(movie.budget),
        "revenue": float(movie.revenue),
        "country": movie.country,
    }


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
):
    total_items_result = await db.execute(select(func.count(MovieModel.id)))
    total_items = total_items_result.scalar() or 0

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page

    query = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = query.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies_dicts = [movie_to_dict(m) for m in movies]

    prev_page = (
        f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"/theater/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return {
        "movies": movies_dicts,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = query.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return movie_to_dict(movie)
