from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.models import MovieModel
from src.database.session import get_db
from src.schemas.movies import MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def movie_router(movie_id: int, db: Session = Depends(get_db)):

    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(status_code=404, detail="No movies found.")
    return movie
