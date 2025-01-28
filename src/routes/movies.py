from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database.session import get_db
from database.models import MovieModel
from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema
)

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(page: int = 1,
               per_page: int = 10,
               db: Session = Depends(get_db)):

    if page < 1 or per_page < 1 or per_page > 20:
        raise HTTPException(status_code=422,
                            detail="Invalid page or per_page values.")

    total_items = db.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = db.query(MovieModel).offset((page - 1) * per_page).limit(
        per_page
    ).all()

    movie_list = [
        MovieDetailResponseSchema.from_orm(movie) for movie in movies
    ]

    prev_page = (f"/movies/?page={page - 1}"
                 f"&per_page={per_page}") if page > 1 else None
    next_page = (f"/movies/?page={page + 1}"
                 f"&per_page={per_page}") if page < total_pages else None

    return MovieListResponseSchema(
        movies=movie_list,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/",
            response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int,
              db: Session = Depends(get_db)) -> dict[list[dict]]:
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404,
                            detail="Movie with the given ID was not found.")

    return movie
