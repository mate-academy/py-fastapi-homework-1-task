import math
from typing import Annotated

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
    status
)

from sqlalchemy import (
    select,
    func,
)
from sqlalchemy.ext.asyncio import AsyncSession
from schemas import (
    MovieListResponseSchema,
    MovieDetailResponseSchema,
)

from database import get_db, MovieModel

router = APIRouter()


@router.get(
    "/movies/",
    response_model=MovieListResponseSchema,
    status_code=status.HTTP_200_OK
)
async def get_movies(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1, description="Page number (minimum: 1)"),
    per_page: int = Query(10, ge=1, le=20, description="Items per page (1-20)")
) -> list[MovieModel]:
    total_movie_items = await db.execute(select(func.count("*")).select_from(MovieModel))
    total_movie_items = total_movie_items.scalar()
    if not total_movie_items:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )
    total_movie_pages = math.ceil(total_movie_items / per_page)
    if total_movie_pages < page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No movies found."
        )

    movie_list = await db.scalars(select(MovieModel).offset((page - 1) * per_page).limit(per_page))
    movie_list = list(movie_list.all())
    movie_list_data = {
        "movies": movie_list,
        "total_pages": total_movie_pages,
        "total_items": total_movie_items
    }
    if page > 1:
        prev_url = f"/theater/movies/?page={page - 1}&per_page={per_page}"
        movie_list_data["prev_page"] = prev_url
    if page < total_movie_pages:
        next_url = f"/theater/movies/?page={page + 1}&per_page={per_page}"
        movie_list_data["next_page"] = next_url

    result = MovieListResponseSchema(
        **movie_list_data
    )
    return result


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema,
    status_code=status.HTTP_200_OK
)
async def get_movie_detail_by_id(
    db: Annotated[AsyncSession, Depends(get_db)],
    movie_id
) -> MovieModel:
    movie = await db.get(MovieModel, movie_id)

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )
    return movie  # noqa
