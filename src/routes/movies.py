import math

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from src.database.models import MovieModel
from src.database.session import get_db
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
        page: int = Query(ge=1, default=1),
        per_page: int = Query(ge=1, le=20, default=10),
        db: Session = Depends(get_db)
):
    movie_query = db.query(MovieModel)
    total_items = movie_query.count()
    movies = movie_query.offset(per_page * (page - 1)).limit(per_page).all()
    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = math.ceil(total_items / per_page)

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    response = {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }
    return response


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
