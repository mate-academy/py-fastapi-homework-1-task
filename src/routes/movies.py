from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, Field

from src.database import get_db, MovieModel
from src.schemas import movies

router = APIRouter(prefix="/movies")


class PaginationParams(BaseModel):
    page: int = Field(ge=1, default=1)
    per_page: int = Field(ge=1, default=10)


@router.get(
    "/", name="get-movies-list", response_model=movies.MovieListResponseSchema
)
async def get_movies_list(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    paginate_query: Annotated[PaginationParams, Query()],
):
    items_count = await session.scalar(func.count(MovieModel.id))
    pages_count = items_count // paginate_query.per_page + 1
    skip = (paginate_query.page - 1) * paginate_query.per_page
    db_movies = await session.scalars(
        select(MovieModel).offset(skip).limit(paginate_query.per_page)
    )
    db_movies = list(db_movies.all())
    if not db_movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found.",
        )

    url = request.url_for("get-movies-list")
    result = movies.MovieListResponseSchema(
        total_pages=pages_count,
        total_items=items_count,
        movies=[
            movies.MovieDetailResponseSchema.model_validate(db_movie)
            for db_movie in db_movies
        ],
        prev_page=(
            str(
                url.include_query_params(
                    page=paginate_query.page - 1,
                    per_page=paginate_query.per_page,
                )
            )
            if paginate_query.page > 1
            else None
        ),
        next_page=(
            str(
                url.include_query_params(
                    page=paginate_query.page + 1,
                    per_page=paginate_query.per_page,
                )
            )
            if paginate_query.page < pages_count
            else None
        ),
    )
    return result


@router.get("/{movie_id}/", response_model=movies.MovieDetailResponseSchema)
async def get_movie_by_id(
    session: Annotated[AsyncSession, Depends(get_db)], movie_id: int
):
    movie = await session.scalar(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return movie
