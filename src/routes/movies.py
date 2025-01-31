import math
from typing import List

from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Query

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: Session = Depends(get_db)
):
    offset = (page - 1) * per_page

    movies = db.query(MovieModel).offset(offset).limit(per_page).all()

    if movies:
        total_items = db.query(MovieModel).count()
        total_pages = math.ceil(total_items / per_page)

        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

        return {
            "movies": movies,
            "prev_page": prev_page,
            "next_page": next_page,
            "total_pages": total_pages,
            "total_items": total_items
        }

    raise HTTPException(status_code=404, detail="No movies found.")


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_detail(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if movie:
        return movie
    raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
