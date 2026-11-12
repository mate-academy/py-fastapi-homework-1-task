from fastapi import APIRouter, Depends, Request

from database.session import get_db, AsyncSQLiteSessionLocal
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema
from crud.movies import get_movie_list


router = APIRouter()

@router.get('/movies/', response_model=MovieListResponseSchema)
async def get_movies(
    request: Request,
    page: int = 1,
    per_page: int = 100,
    db: AsyncSQLiteSessionLocal = Depends(get_db)
):
    movies, total_items = await get_movie_list(db, page, per_page)

    total_pages = round(total_items / per_page)

    prev_page = None
    next_page = None

    if page > 1:
        prev_page = str(request.url.include_query_params(page=page - 1, per_page=per_page))

    if page < total_pages:
        next_page = str(request.url.include_query_params(page=page + 1, per_page=per_page))

    return MovieListResponseSchema(
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
        movies=[MovieDetailResponseSchema.model_validate(movie) for movie in movies],
    )
