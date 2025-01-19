from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel

from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies", response_model=MovieListResponseSchema)
def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: Session = Depends(get_db)
):
    skip = (page - 1) * per_page

    movies = db.query(MovieModel).offset(skip).limit(per_page).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_items = db.query(MovieModel).count()

    if total_items % per_page == 0:
        total_pages = total_items // per_page
    else:
        total_pages = (total_items // per_page) + 1

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    movie_details = [MovieDetailResponseSchema.model_validate(movie) for movie in movies]

    return MovieListResponseSchema(
        movies=movie_details,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
