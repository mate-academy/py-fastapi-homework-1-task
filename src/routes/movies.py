from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database import get_db, MovieModel
from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

from fastapi_pagination import Page, paginate

router = APIRouter()


@router.get("/movies/", response_model=Page[MovieListResponseSchema])
def get_paginated_movies(db: Session = Depends(get_db), page: int = 1, size: int = 10):

    movies = db.query(MovieModel).all()
    start = (page - 1) * size
    end = start + size

    return paginate(movies[start:end])


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_detail_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie
