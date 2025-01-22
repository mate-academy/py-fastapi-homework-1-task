import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database import get_db, MovieModel
from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
    page: int = Query(ge=1, default=1),
    per_page: int = Query(ge=1, le=20, default=10),
    db: Session = Depends(get_db),
):
    movie = db.query(MovieModel)
    total_items = movie.count()
    total_pages = math.ceil(total_items / per_page)
    offset = (page - 1) * per_page
    movies = movie.offset(offset).limit(per_page).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = f"/theater/movies/?page={max(1, page - 1)}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={min(total_pages, page + 1)}&per_page={per_page}"\
        if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
