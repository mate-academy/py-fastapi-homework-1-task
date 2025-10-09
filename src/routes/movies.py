from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from database import get_db, MovieModel
import math


router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_film(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return film


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_all_films(db: AsyncSession = Depends(get_db),
                        page: int = Query(1, ge=1),
                        per_page: int = Query(10, ge=1, le=20)
                        ):
    movies_result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset((page - 1) * per_page)
        .limit(per_page)
    )
    movies = movies_result.scalars().all()
    if not movies:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found.",
        )

    total_items = int(await db.scalar(select(func.count()).select_from(MovieModel)))
    total_pages = math.ceil(total_items / per_page)

    return MovieListResponseSchema(
        movies=movies,
        prev_page=f"/theater/movies/?page={max(1, page - 1)}&per_page={per_page}"
        if page > 1 else None,
        next_page=f"/theater/movies/?page={min(total_pages, page + 1)}&per_page={per_page}"
        if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items,
    )
