from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/movies", response_model=MovieListResponseSchema)
def read_movies(
    page: Annotated[int, Query(ge=1)] = 1,
    per_page: Annotated[int, Query(ge=1, le=20)] = 10,
    db: Session = Depends(get_db)
) -> MovieListResponseSchema:
    offset = (page - 1) * per_page
    limit = per_page

    total_items = db.query(MovieModel).count()
    movies = db.query(MovieModel).offset(offset).limit(limit).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    prev_page = None
    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    next_page = None
    if page < total_pages:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get(
    "/movies/{movie_id}",
    response_model=MovieDetailResponseSchema
)
def read_movie(
    movie_id: int,
    db: Session = Depends(get_db)
) -> MovieDetailResponseSchema:
    movie = db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
