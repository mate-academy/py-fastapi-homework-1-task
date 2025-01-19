from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
        page: int = Query(1, ge=1, description="The page number to fetch"),
        per_page: int = Query(10, ge=1, le=20, description="Number of movies per page"),
        db: Session = Depends(get_db)
):
    if page < 1:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "page"],
                    "msg": "ensure this value is greater than or equal to 1",
                    "type": "value_error.number.not_ge"
                }
            ]
        )

    if per_page < 1 or per_page > 20:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "per_page"],
                    "msg": "ensure this value is between 1 and 20",
                    "type": "value_error.number.not_in_range"
                }
            ]
        )

    movies = db.query(MovieModel)
    total_items = movies.count()
    total_pages = ceil(total_items / per_page)

    offset = (page - 1) * per_page
    movies_query = movies.offset(offset).limit(per_page).all()

    if not movies_query:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies_data = [MovieDetailResponseSchema.from_orm(movie) for movie in movies_query]

    prev_page = (
        f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    )
    next_page = (
        f"/theater/movies/?page={page + 1}&per_page={per_page}"
        if page < total_pages
        else None
    )

    return MovieListResponseSchema(
        movies=movies_data,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
