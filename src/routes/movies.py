from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from database import get_db, MovieModel

from schemas import MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(page: int, per_page: int = 10, db: Session = Depends(get_db)):
    if page < 1:
        raise HTTPException(
            status_code=422,
            detail="ensure this value is greater than or equal to 1"
        )
    if not 1 <= per_page <= 20:
        raise HTTPException(
            status_code=422,
            detail="ensure this value is greater than or equal to 1 and smaller than 21"
        )
    start_id = (page * per_page) - per_page
    end_id = page * per_page
    query_set = db.query(MovieModel).all()
    movies = [movie for movie in query_set if start_id < movie.id <= end_id]
    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )
    total_pages = len(query_set) // per_page if len(query_set) % per_page == 0 else (len(query_set) // per_page) + 1
    base_page_url = "/api/v1/theater/movies/"
    response_for = {
        "movies": movies,
        "total_items": f"{len(query_set)}",
        "total_pages": total_pages
    }
    if total_pages > page:
        response_for["next_page"] = f"{base_page_url}?page={page + 1}&per_page={per_page}"
    if page > 1:
        response_for["prev_page"] = f"{base_page_url}?page={page - 1}&per_page={per_page}"
    return response_for


@router.get("/movies/{movie_id}")
def get_detail_movie_page(movie_id: int, db: Session = Depends(get_db)):
    response = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not response:
        raise HTTPException(status_code=404, detail=f"Movie with the given ID {movie_id} was not found.")
    return response
