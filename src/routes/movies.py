from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.database.models import MovieModel

from typing import List, Optional
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: Session = Depends(get_db)
):
    total_items = db.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = db.query(MovieModel).offset((page - 1) * per_page).limit(per_page).all()

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    # Перетворення SQLAlchemy об'єктів на Pydantic моделі
    movies = [MovieDetailResponseSchema.model_validate({
        **movie.__dict__,
        "date": movie.date.isoformat() if isinstance(movie.date, date) else movie.date,
        "revenue": int(movie.revenue) if isinstance(movie.revenue, float) else movie.revenue
    }) for movie in movies]

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.model_validate({
        **movie.__dict__,
        "date": movie.date.isoformat() if isinstance(movie.date, date) else movie.date,
        "revenue": int(movie.revenue) if isinstance(movie.revenue, float) else movie.revenue
    })
