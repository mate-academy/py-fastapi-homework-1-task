import math

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
        db: Session = Depends(get_db),
        page: int = 1,
        per_page: int = 10
):
    # Calculate offset for pagination
    offset = (page - 1) * per_page
    # Fetch paginated movies and total count
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()
    total_items = db.query(MovieModel).count()

    # Validate page and per_page parameters
    if page < 1 or per_page < 1:
        raise HTTPException(
            status_code=422,
            detail=[{"msg": "Input should be greater than or equal to 1"}],
        )

    total_pages = math.ceil(total_items / per_page)

    if not movies or page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    return {
        "movies": movies,
        "prev_page": (
            None
            if page == 1
            else f"/theater/movies/?page={page - 1}&per_page={per_page}"
        ),
        "next_page": (
            f"/theater/movies/?page={page + 1}&per_page={per_page}"
            if page < total_pages
            else None
        ),
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_detail_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
