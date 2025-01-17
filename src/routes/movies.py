from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies", response_model=MovieListResponseSchema)
def get_list_movies(page: int = Query(default=1, ge=1),
                    per_page: int = Query(default=10, ge=1, le=20),
                    db: Session = Depends(get_db)
                    ):
    offset = (page - 1) * per_page
    movies_with_pagination = db.query(MovieModel).offset(offset).limit(per_page).all()
    movie_list_schema = [
        MovieDetailResponseSchema.model_validate(movie) for movie in movies_with_pagination
    ]
    total_items = db.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page
    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    if not movie_list_schema:
        raise HTTPException(status_code=404, detail="No movies found.")

    return MovieListResponseSchema(
        movies=movies_with_pagination,
        total_items=total_items,
        total_pages=total_pages,
        prev_page=None if page == 1 else prev_page,
        next_page=None if page == total_pages else next_page,
    )


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
