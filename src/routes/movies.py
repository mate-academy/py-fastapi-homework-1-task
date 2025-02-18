from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Annotated

from ..database import get_db, MovieModel
from ..schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_film(movie_id: int, db: Session = Depends(get_db)):
    film = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return film


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_films(
        page: Annotated[int, Query(ge=1)] = 1,
        per_page: Annotated[int, Query(ge=1, le=20)] = 10,
        db: Session = Depends(get_db)
):
    films = db.query(MovieModel).offset((page - 1) * per_page).limit(per_page)
    total_items = db.query(MovieModel).count()
    total_pages = -int(-(total_items / per_page) // 1)
    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")
    return {
        "movies": films,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }
