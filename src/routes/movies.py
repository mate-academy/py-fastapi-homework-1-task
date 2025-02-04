from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from src.database.session import get_db
from src.database.models import MovieModel


router = APIRouter()


@router.get("/movies", response_model=MovieListResponseSchema)
def get_movies(
    page: int = Query(1, ge=1, description="Page number to fetch"),
    per_page: int = Query(10, ge=1, le=20, description="Number per page"),
    db: Session = Depends(get_db),
):

    total_items = db.query(MovieModel).count()
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()

    prev_page = (
        f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"/theater/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie_details(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
