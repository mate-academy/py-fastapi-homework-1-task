from typing import List, Dict, Union, Optional, Annotated
from math import ceil
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from src.database import get_db, MovieModel

from src.schemas.movies import MovieListResponseSchema, MovieDetailsResponseSchema

router = APIRouter()


@router.get(
    "/movies/",
    response_model=Dict[str, Union[List[MovieListResponseSchema], Optional[str], int]]
)
def movies(
        db: Session = Depends(get_db),
        page: Annotated[int, Query(..., title="The page number to fetch", ge=1)] = 1,
        per_page: Annotated[int, Query(
            ...,title="Number of movies to fetch per page", ge=1, le=20
        )]  = 10
) -> Dict[str, Union[List[MovieListResponseSchema], Optional[str], int]]:

    data = db.query(MovieModel).all()

    total_pages = ceil(len(data) / per_page)

    start = (page - 1) * per_page
    end = start + per_page

    items = len(data)
    if not items or page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    if end >= items:
        next_page = None
    else:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"
    if page == 1:
        prev_page = None
    else:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"

    response = {
        "movies": data[start:end],
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": items
    }

    return response


@router.get("/movies/{movie_id}/", response_model=MovieDetailsResponseSchema)
def get_movie(movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
