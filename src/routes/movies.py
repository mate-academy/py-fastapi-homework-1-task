from fastapi import APIRouter, HTTPException, Request
from sqlalchemy import select, func

from database import MovieModel, models
from dependencies import DB, PaginationDep
from schemas.movies import MoviesPageSchema, MovieDetailResponseSchema

router = APIRouter(prefix="/movies", tags=["movies"])


@router.get(
    path="/",
    response_model=MoviesPageSchema,
)
async def get_movies(request: Request, db: DB, pagination: PaginationDep):
    total_items = await db.scalar(select(func.count()).select_from(MovieModel))
    total_pages = pagination.total_pages(total_items)

    db_movies = await db.execute(
        select(MovieModel).offset(pagination.offset).limit(pagination.limit)
    )

    movies = db_movies.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    base_path = request.url.path

    return MoviesPageSchema(
        movies=movies,
        prev_page=(
            pagination.build_page_url(base_path, pagination.page - 1)
            if pagination.page > 1
            else None
        ),
        next_page=(
            pagination.build_page_url(base_path, pagination.page + 1)
            if pagination.page < total_pages
            else None
        ),
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get(
    path="/{movie_id}/",
    response_model=MovieDetailResponseSchema,
)
async def get_movie(movie_id: int, db: DB):
    db_movie = await db.scalar(
        select(models.MovieModel).where(models.MovieModel.id == movie_id)
    )

    if not db_movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return db_movie
