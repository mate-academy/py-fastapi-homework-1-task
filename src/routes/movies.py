from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Params
from fastapi_pagination.ext.sqlalchemy import paginate

from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):
    params = Params(page=page, size=per_page)
    stmt = select(MovieModel).order_by(MovieModel.id.asc())
    pg = await paginate(db, stmt, params=params)

    total_items = pg.total
    total_pages = pg.pages

    if total_items == 0 or page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    prev_page = None if page <= 1 else f"/theater/movies/?page={page - 1}&per_page={per_page}"
    next_page = None if page >= total_pages else f"/theater/movies/?page={page + 1}&per_page={per_page}"

    return MovieListResponseSchema(
        movies=pg.items,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie_by_id(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):
    movie = await db.get(MovieModel, movie_id)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return MovieDetailResponseSchema.model_validate(movie)
