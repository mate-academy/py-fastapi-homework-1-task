from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: Session = Depends(get_db)
):
    skip = (page - 1) * per_page
    limit = per_page

    films = db.query(MovieModel).offset(skip).limit(limit).all()

    if not films:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_items = db.query(MovieModel).count()
    total_pages = ceil(total_items / per_page)

    root = "/theater"

    prev_page = f"{root}/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{root}/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=films,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/")
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
