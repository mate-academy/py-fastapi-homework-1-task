from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from math import ceil

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(default=1, ge=1, description="Page number"),
    per_page: int = Query(default=10, ge=1, le=20, description="Items per page"),
    db: Session = Depends(get_db),
):
    # Get total count for pagination
    total_items = db.query(MovieModel).count()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Calculate pagination values
    total_pages = ceil(total_items / per_page)
    offset = (page - 1) * per_page

    # Get movies for current page
    movies = (
        db.query(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
        .all()
    )

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Generate pagination links
    base_url = "/theater/movies/"
    prev_page = f"{base_url}?page={page-1}&per_page={per_page}" if page > 1 else None
    next_page = (
        f"{base_url}?page={page+1}&per_page={per_page}" if page < total_pages else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return movie
