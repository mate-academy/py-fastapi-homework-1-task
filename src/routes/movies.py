from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel

router = APIRouter()


@router.get("/movies/", response_model=dict)
def get_movies(
        db: Session = Depends(get_db),
        page: int = Query(
            default=1,
            ge=1,
            description="Page number, starting from 1"
        ),
        per_page: int = Query(
            default=10,
            ge=1,
            le=20,
            description="Number of movies per page"
        )
):
    offset = (page - 1) * per_page

    total_items = db.query(MovieModel).count()
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    prev_page = (f"/theater/movies/?page={page - 1}"
                 f"&per_page={per_page}") if page > 1 else None
    next_page = (f"/theater/movies/?page={page + 1}"
                 f"&per_page={per_page}") if page < total_pages else None

    return {
        "movies": [
            MovieDetailResponseSchema.model_validate(movie) for movie in movies
        ],
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get(
    "/movies/{movie_id}",
    response_model=MovieDetailResponseSchema
)
def get_film(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
