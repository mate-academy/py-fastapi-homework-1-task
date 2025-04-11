from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import get_db, Movie
from src.schemas import MovieListResponseSchema
from src.schemas.movies import MovieCreate, MovieDetailResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1, description="The page number to fetch."),
    per_page: int = Query(10, ge=1, le=20, description="Number of movies to fetch per page."),
    db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page

    result_count = await db.execute(select(func.count(Movie.id)))
    total_movies = result_count.scalar()

    result = await db.execute(select(Movie).limit(per_page).offset(offset))
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_movies + per_page - 1) // per_page

    prev_page = None
    next_page = None

    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    if page < total_pages:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_movies
    )


@router.post("/movies/", response_model=MovieDetailResponseSchema)
async def create_movie(film: MovieCreate, db: AsyncSession = Depends(get_db)):
    new_film = Movie(**film.model_dump())

    db.add(new_film)
    await db.commit()
    await db.refresh(new_film)

    return new_film


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_film(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Movie).where(Movie.id == movie_id))
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
