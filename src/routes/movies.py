from math import ceil

from fastapi import APIRouter, HTTPException, Depends, Query
from sqlalchemy.orm import Session

from src.database import get_db, MovieModel
from src.routes.exceptions import (
    validate_page,
    validate_per_page,
    validate_movies_exist
)
from src.schemas.movies import (
    MovieListResponseSchema,
    MovieDetailResponseSchema,
)

router = APIRouter()


def get_pagination_url(page: int, per_page: int) -> str:
    return f"/theater/movies/?page={page}&per_page={per_page}"


@router.get("/movies", response_model=MovieListResponseSchema)
def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    validate_page(page)
    validate_per_page(per_page)

    offset = (page - 1) * per_page
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()
    validate_movies_exist(movies)

    total_items = db.query(MovieModel).count()
    total_pages = ceil(total_items / per_page)
    prev_page = get_pagination_url(page - 1, per_page) if page > 1 else None
    next_page = (
        get_pagination_url(page + 1, per_page)
        if page < total_pages else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get(
    "/movies/{movie_id}",
    response_model=MovieDetailResponseSchema
)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return movie
