from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from database import get_db
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from database.models import MovieModel

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(page: int = 1, per_page: int = 10, db: AsyncSession = Depends(get_db)):
    if page < 1 or per_page < 1 or per_page > 20:
        raise HTTPException(status_code=422, detail="Invalid query parameters.")

    offset = (page - 1) * per_page
    result = await db.execute(select(MovieModel).offset(offset).limit(per_page))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_items = await db.execute(select([func.count()]).select_from(MovieModel))
    total_items = total_items.scalar()
    total_pages = (total_items + per_page - 1) // per_page

    prev_page = f"/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=[MovieDetailResponseSchema.from_orm(movie) for movie in movies],
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).filter(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema.from_orm(movie)
