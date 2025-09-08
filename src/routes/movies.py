from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.models import MovieModel
from database.session import get_db
from schemas.movies import (
    MovieDetailResponseSchema,
    MovieListResponseSchema
)


router = APIRouter(prefix="/movies")


@router.get(path="/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(movie_id == MovieModel.id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )
    return movie


@router.get(path="/", response_model=MovieListResponseSchema)
async def get_movies(
    db: AsyncSession = Depends(get_db),
    page: int = Query(
        default=1,
        ge=1,
        description="Page number, must be >= 1"
    ),
    per_page: int = Query(
        default=10,
        ge=1,
        le=20,
        description="Items per page, must be between 1 and 20"
    )
):
    total_items_result = await db.execute(
        select(func.count()).select_from(MovieModel)
    )
    total_items = total_items_result.scalar()
    if total_items == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )
    total_pages = (total_items + per_page - 1) // per_page
    offset = (page - 1) * per_page
    if offset >= total_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    base_url = "/theater/movies/"
    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}"
        if page > 1 else None
    )
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages else None
    )

    result_movies = await db.execute(
        select(MovieModel)
        .limit(per_page)
        .offset(offset)
        .order_by(MovieModel.id)
    )
    movies = result_movies.scalars().all()
    movie_schemas = [
        MovieDetailResponseSchema.model_validate(movie)
        for movie in movies
    ]

    return MovieListResponseSchema(
        movies=movie_schemas,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )
