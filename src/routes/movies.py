from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_all_movies(
        request: Request,
        page: Annotated[int, Query(ge=1)] = 1,
        per_page: Annotated[int, Query(ge=1, le=20)] = 10,
        db: Session = Depends(get_db),
) -> MovieListResponseSchema:
    start = (page - 1) * per_page
    films = db.query(MovieModel).offset(start).limit(per_page).all()

    total_items = db.query(MovieModel).count()
    total_pages = (total_items + per_page - 1) // per_page

    prev_page = None
    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    next_page = None
    if page < total_pages:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"

    if not films:
        raise HTTPException(status_code=404, detail="No movies found.")

    return MovieListResponseSchema(
        movies=films,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movies_id}/", response_model=MovieDetailResponseSchema)
def get_single_movie(
        movies_id: int,
        db: Session = Depends(get_db)
) -> MovieDetailResponseSchema:
    film = db.get(MovieModel, movies_id)

    if not film:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found.",
        )

    return film
