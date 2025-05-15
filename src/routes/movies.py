from fastapi import APIRouter, Query, Request, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema


router = APIRouter()


@router.get(
    "/movies/",
    response_model=MovieListResponseSchema,
    summary="Get paginated list of movies",
)
async def list_movies(
    request: Request,
    page: int = Query(1, ge=1, description="Page number"),
    per_page: int = Query(10, ge=1, le=20, description="Movies per page"),
    db: AsyncSession = Depends(get_db),
):
    total_items = (
        await db.execute(select(func.count()).select_from(MovieModel))
    ).scalar()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages and total_items > 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel).offset(offset).limit(per_page)
    )
    movies = result.scalars().all()

    base_url = str(request.url).split("?")[0]

    def params(p: int) -> str:
        return f"?page={p}&per_page={per_page}"

    prev_page = f"{base_url}{params(page - 1)}" if page > 1 else None
    next_page = f"{base_url}{params(page + 1)}" if page < total_pages else None

    return {
        "movies": [
            MovieDetailResponseSchema.model_validate(movie) for movie in movies
        ],
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema,
    summary="Get details of a movie by ID",
)
async def get_movie_details(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MovieModel).filter(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )

    return MovieDetailResponseSchema.model_validate(movie)
