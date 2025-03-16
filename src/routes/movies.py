import math

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/", response_model=MovieListResponseSchema)
def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db),
):
    total_items = db.query(MovieModel).count()
    total_pages = math.ceil(total_items / per_page)

    if total_items == 0:
        raise HTTPException(status_code=404, detail="Not found")

    movies = (
        db.query(MovieModel)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .all()
    )

    return {
        "movies": movies,
        "prev_page": page - 1 if page > 1 else 0,
        "next_page": page + 1 if page < total_pages else None,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Not found")
    return movie
