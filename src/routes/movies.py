from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    Query
)
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas import (
    MovieListResponseSchema,
    MovieDetailResponseSchema
)
from src.database import get_db, MovieModel


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        request: Request,
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100),
):
    curr_offset = (page - 1) * per_page
    movies_result = await db.execute(select(MovieModel).offset(curr_offset).limit(per_page))
    movies = movies_result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found.")

    count_result = await db.execute(select(func.count()).select_from(MovieModel))
    total_movies = count_result.scalar()
    total_pages = (total_movies + per_page - 1) // per_page

    url_path = request.url.path
    query_base = f"{url_path}?per_page={per_page}"

    prev_page = f"{query_base}&page={page - 1}" if page > 1 else None
    next_page = f"{query_base}&page={page + 1}" if page < total_pages else None

    return {
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_movies,
        "movies": movies
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    movie = result.scalar_one_or_none()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
