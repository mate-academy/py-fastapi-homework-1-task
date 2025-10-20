import math
from decimal import Decimal
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from database.session import get_db
from database.models import MovieModel
from schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter(prefix="/movies", tags=["Movies"])
LINK_PREFIX = "/theater/movies/"


def to_movie_schema(m: MovieModel) -> MovieDetailResponseSchema:
    return MovieDetailResponseSchema(
        id=m.id,
        name=m.name,
        date=m.date,
        score=m.score,
        genre=m.genre,
        overview=m.overview,
        crew=m.crew,
        orig_title=m.orig_title,
        status=m.status,
        orig_lang=m.orig_lang,
        budget=int(m.budget) if not isinstance(m.budget, Decimal) else int(m.budget),
        revenue=int(m.revenue),
        country=m.country,
    )


def build_link(base: str, page: int, per_page: int) -> str:
    return f"{base}?page={page}&per_page={per_page}"


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
    page: int = Query(1, ge=1, description="The page number to fetch"),
    per_page: int = Query(10, ge=1, le=20, description="Number of movies per page"),
    db: AsyncSession = Depends(get_db),
):
    total_items = (await db.execute(select(func.count()).select_from(MovieModel))).scalar_one()
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")
    total_pages = max(1, math.ceil(total_items / per_page))
    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")
    offset = (page - 1) * per_page
    result = await db.execute(
        select(MovieModel)
        .order_by(MovieModel.id)
        .offset(offset)
        .limit(per_page)
    )
    movies_db = result.scalars().all()
    movies = [to_movie_schema(m) for m in movies_db]
    prev_page = None if page == 1 else build_link(LINK_PREFIX, page - 1, per_page)
    next_page = None if page == total_pages else build_link(LINK_PREFIX, page + 1, per_page)
    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items,
    )


@router.get("/{movie_id}/", response_model=MovieDetailResponseSchema, status_code=status.HTTP_200_OK)
async def get_movie_detail(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(MovieModel, movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return to_movie_schema(movie)
