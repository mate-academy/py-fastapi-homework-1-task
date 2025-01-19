import math

from fastapi import APIRouter, Depends, HTTPException, Query
from schemas.movies import MoviesSchema, MovieShema
from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.sql.annotation import Annotated

from database import get_db, MovieModel


router = APIRouter()


@router.get("/movies")
def read_movies(
        db: Session = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
) -> MoviesSchema:
    total_items = db.query(MovieModel).count()
    total_pages = math.ceil(total_items / per_page)
    if not total_items or page > total_pages:
        raise HTTPException(404, "No movies found.")
    count = (page - 1) * per_page
    movies = (
        db
        .query(MovieModel)
        .offset(count)
        .limit(per_page)
        .all()
    )

    prev_page = None
    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    next_page = None
    if page < 20 and total_items > count:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    movieschemas = [
        MovieShema(
            id=movie.id,
            name=movie.name,
            date=movie.date,
            score=movie.score,
            genre=movie.genre,
            overview=movie.overview,
            crew=movie.crew,
            orig_title=movie.orig_title,
            status=movie.status,
            orig_lang=movie.orig_lang,
            budget=movie.budget,
            revenue=movie.revenue,
            country=movie.country,
        ) for movie in movies
    ]

    return MoviesSchema(
        movies=movieschemas,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movie_id}")
def read_movie(
        movie_id: int,
        db: Session = Depends(get_db),
) -> MovieShema:
    movie = db.query(MovieModel).get(movie_id)
    if not movie:
        raise HTTPException(404, "Movie with the given ID was not found.")
    return MovieShema(
        id=movie.id,
        name=movie.name,
        date=movie.date,
        score=movie.score,
        genre=movie.genre,
        overview=movie.overview,
        crew=movie.crew,
        orig_title=movie.orig_title,
        status=movie.status,
        orig_lang=movie.orig_lang,
        budget=movie.budget,
        revenue=movie.revenue,
        country=movie.country,
    )
