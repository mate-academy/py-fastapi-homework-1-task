from fastapi import APIRouter, Depends, Request, Query, HTTPException
from sqlalchemy import select

from database.session import get_db, AsyncSQLiteSessionLocal
from database.models import MovieModel

from pagination.utils import paginate
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()


@router.get('/movies/', response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    page: int = Query(default=1, ge=1),
    per_page: int = Query(default=10, ge=1, le=20),
    db: AsyncSQLiteSessionLocal = Depends(get_db)
):
    (
        movies,
        total_items,
        total_pages,
        prev_page,
        next_page
    ) = await paginate(
        db,
        MovieModel,
        request,
        page,
        per_page
    )

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    return MovieListResponseSchema(
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
        movies=[MovieDetailResponseSchema.model_validate(movie) for movie in movies],
    )


@router.get('/movies/{movie_id}/', response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSQLiteSessionLocal = Depends(get_db)):
    movie_selection = select(MovieModel).where(MovieModel.id == movie_id)

    selection_result = await db.execute(movie_selection)
    movie = selection_result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema.model_validate(movie)
