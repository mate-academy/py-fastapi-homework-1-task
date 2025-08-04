from fastapi import APIRouter, Depends, HTTPException, Request, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database.session import get_db
from database.models import MovieModel

from schemas.movies import MovieListResponseSchema, MovieRead, MovieDetailResponseSchema


router = APIRouter()


@router.get("/movies", response_model=MovieListResponseSchema)
async def get_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=20),
        db: AsyncSession = Depends(get_db),
):

    total_items_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_items = total_items_result.scalar()
    total_pages = (total_items + per_page - 1) // per_page

    base_url = str(request.url).split("?")[0]
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None

    offset = (page - 1) * per_page
    result = await db.execute(
        select(MovieModel).offset(offset).limit(per_page)
    )
    movies = result.scalars().all()

    return MovieListResponseSchema(
        movies=[MovieRead.from_orm(m) for m in movies],
        prev_page=prev_page,
        next_page=next_page,
        total_pages=total_pages,
        total_items=total_items
    )


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return MovieDetailResponseSchema.from_orm(movie)
