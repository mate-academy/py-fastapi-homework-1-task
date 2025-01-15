import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel
from schemas.movies import MovieList, MovieDetail


router = APIRouter()


@router.get("/movies/", response_model=MovieList)
def get_movies(
        db: Session = Depends(get_db),
        page: int = Query(ge=1, default=1),
        per_page: int = Query(ge=1, le=20, default=10)
):
    total_items = db.query(MovieModel).count()
    total_pages = math.ceil(total_items / per_page)

    first_element = (page - 1) * per_page
    last_element = page * per_page

    movies = db.query(MovieModel).slice(first_element, last_element).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieList(
        movies=[MovieDetail.from_orm(movie) for movie in movies],
        prev_page=prev_page if page > 1 else None,
        next_page=next_page if page < total_pages else None,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetail)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
