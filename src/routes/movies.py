from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel

from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()



@router.get("/movies")
def get_list_movies():
    return {"Hello": "World"}

#         # page: int = Query(default=1, ge=1, description="Номер страницы (>= 1)"),
#         # per_page: int = Query(default=10, ge=1, le=20, description="Количество фильмов на странице (>= 1 и <= 20)"),
#         db: Session = Depends(get_db)
# ):
#     # total_items = db.query(MovieModel).count()
#     # if total_items == 0:
#     #     raise HTTPException(status_code=404, detail="No movies found.")
#     #
#     # offset = (page - 1) * per_page
#
#     movies = db.query(MovieModel).all()
#     if movies:
#         raise HTTPException(status_code=200, detail=movies)
#
#     return movies


# @router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
# def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
#     movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
#
#     return movie