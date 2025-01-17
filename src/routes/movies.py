from typing import Type
from sqlalchemy.orm import Session
from database import get_db, MovieModel

from fastapi import (
    APIRouter,
    HTTPException,
    Depends,
    Query
)
from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema
)


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def read_movies(
        page: int = Query(ge=1, default=1),
        per_page: int = Query(ge=1, default=10),
        db: Session = Depends(get_db)
) -> MovieListResponseSchema:

    total_items = db.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page

    offset = (page - 1) * per_page
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    base_url = "/theater/movies/"
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)) -> Type[MovieModel]:
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
