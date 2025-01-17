from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema
from database.models import MovieModel


router = APIRouter()


@router.get("/movies", response_model=MovieListResponseSchema)
def get_movies(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1), db: Session = Depends(get_db)):
    movies = db.query(MovieModel).offset((page - 1) * per_page).limit(per_page).all()
    total_movies = db.query(MovieModel).count()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")
    if (page and page < 1):
        raise HTTPException(
            status_code=422,
            detail=[
                {
                  "loc": ["query", "page"],
                  "msg": "ensure this value is greater than or equal to 1",
                  "type": "value_error.number.not_ge"
                }
            ]
        )
    return {
        "movies": movies,
        "prev_page": f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None,
        "next_page": f"/theater/movies/?page={page + 1}&per_page={per_page}" if total_movies > (page * per_page) else None,
        "total_pages": (total_movies // per_page) + (1 if total_movies % per_page > 0 else 0),
        "total_items": total_movies,
    }


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
