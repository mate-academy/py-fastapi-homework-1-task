from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()

@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: Session = Depends(get_db)
):
    offset = (page - 1) * per_page
    movies_query = db.query(MovieModel).offset(offset).limit(per_page).all()
    total_items = db.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page

    if not movies_query:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = [
        MovieDetailResponseSchema(
            id=movie.id,
            name=movie.name,
            date=movie.date.isoformat(),
            score=movie.score,
            genre=movie.genre,
            overview=movie.overview,
            crew=movie.crew,
            orig_title=movie.orig_title,
            status=movie.status,
            orig_lang=movie.orig_lang,
            budget=movie.budget,
            revenue=movie.revenue,
            country=movie.country
        )
        for movie in movies_query
    ]

    prev_page = f"/theater/movies/?page={page-1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page+1}&per_page={per_page}" if page < total_pages else None

    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema(
        id=movie.id,
        name=movie.name,
        date=movie.date.isoformat(),
        score=movie.score,
        genre=movie.genre,
        overview=movie.overview,
        crew=movie.crew,
        orig_title=movie.orig_title,
        status=movie.status,
        orig_lang=movie.orig_lang,
        budget=movie.budget,
        revenue=movie.revenue,
        country=movie.country
    )
