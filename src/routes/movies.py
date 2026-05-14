from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query
)
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(default=1, ge=1),
        per_page: int = Query(default=10, ge=1, le=20),
) -> dict:

    total_items = await db.scalar(
        select(func.count()).select_from(MovieModel)
    )
    total_pages = (total_items + per_page - 1) // per_page

    movies = await db.execute(
        select(MovieModel).limit(per_page).offset((page - 1) * per_page)
    )
    movies = movies.scalars().all()
    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )
    return {
        "movies": movies,
        "prev_page": f"/theater/movies/?page={page - 1}&"
                     f"per_page={per_page}" if page > 1 else None,
        "next_page": f"/theater/movies/?page={page + 1}&"
                     f"per_page={per_page}" if page < total_pages else None,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
) -> MovieDetailResponseSchema:
    db_movie = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie_detail = db_movie.scalars().first()
    if not movie_detail:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie_detail
