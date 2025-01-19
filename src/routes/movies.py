from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

from database import get_db, MovieModel


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, le=20, ge=1),
        db: Session = Depends(get_db)
) -> MovieListResponseSchema:
    total_items = db.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page

    offset = (page - 1) * per_page
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = (f"/theater/movies/?page={page - 1}"
                 f"&per_page={per_page}") if page > 1 else None
    next_page = (f"/theater/movies/?page={page + 1}"
                 f"&per_page={per_page}") if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie_details(movie_id: int, db: Session = Depends(get_db)) -> MovieDetailResponseSchema:
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return MovieDetailResponseSchema.model_validate(movie)
