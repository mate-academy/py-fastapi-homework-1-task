from fastapi import APIRouter, Depends, Request

from database.session import get_db, AsyncSQLiteSessionLocal
from database.models import MovieModel

from pagination.utils import paginate
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()

@router.get('/movies/', response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    page: int = 1,
    per_page: int = 100,
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

    return MovieListResponseSchema(
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
        movies=[MovieDetailResponseSchema.model_validate(movie) for movie in movies],
    )
