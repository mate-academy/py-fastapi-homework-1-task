from math import ceil

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.sql import func

from database import get_db, MovieModel
from schemas.movies import PaginatedMovies, MovieSchema

router = APIRouter()


@router.get("/movies/{movie_id}")
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie


@router.get("/movies/", response_model=PaginatedMovies)
def get_movies(
        page: int = 1,
        per_page: int = 10,
        db: Session = Depends(get_db)
):

    if page < 1 or (per_page < 1 or per_page > 20):
        raise HTTPException(
            status_code=422,
            detail=[{"msg": "Input should be greater than or equal to 1"}]
        )

    total_items = db.query(func.count(MovieModel.id)).scalar()
    total_pages = ceil(total_items / per_page)

    if page > total_pages:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    movie_list = db.query(MovieModel).offset((page - 1) * per_page).limit(per_page).all()

    movies = [MovieSchema.model_validate(movie) for movie in movie_list]

    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )

    return {
        "movies": movies,
        "prev_page": f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "next_page": f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None,
        "total_pages": total_pages,
        "total_items": total_items,
    }
