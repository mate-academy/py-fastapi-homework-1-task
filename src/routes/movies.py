from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.models import MovieModel
from database.session import get_db
from schemas.movies import MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def movie_router(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found."
)
    return movie



#PAGINATION
# @router.get("/movies/{film_id}", response_model=PagedResponseSchema[MovieDetailResponseSchema])

