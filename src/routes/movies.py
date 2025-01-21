import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List

from src.database.models import MovieModel
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from src.database.session import get_db

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1)
):

    movies = db.query(MovieModel).offset((page - 1) * per_page).limit(per_page).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_items = db.query(MovieModel).count()
    total_pages = math.ceil(total_items / per_page)

    prev_page = (f"/theater/movies/?page={page - 1 if page > 0 else None}"
                 f"&per_page={per_page}") if page - 1 > 0 else None

    next_page = (f"/theater/movies/?page={page + 1 if page < total_pages else None}"
                 f"&per_page={per_page}") if page - 1 < total_pages else None

    return MovieListResponseSchema(
        movies=[MovieDetailResponseSchema.from_orm(movie) for movie in movies],
        prev_page=prev_page,
        next_page=next_page,
        total_items=total_items,
        total_pages=total_pages)


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.from_orm(movie)
