from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel

from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()



@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
        page: int = Query(default=1, ge=1, description="The page number(>= 1)"),
        per_page: int = Query(default=10, ge=1, le=20, description="Film quantity at the page (>= 1 и <= 20)"),
        db: Session = Depends(get_db)
):
    total_items = db.query(MovieModel).count()
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")
    offset = (page - 1) * per_page
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()
    base_url = "/movies/"
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if offset + per_page < total_items else None
    if page is None or per_page is None:
        raise HTTPException(status_code=422, detail="Ensure this value is greater than or equal to 1")
    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": (total_items + per_page - 1) // per_page,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie