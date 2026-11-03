from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieDetailResponseSchema, MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(page: int = 1, per_page: int = 10, session: AsyncSession = Depends(get_db)):
    if page < 1:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "page"],
                    "msg": "Input should be greater than or equal to 1",
                    "type": "value_error.number.not_ge"
                }
            ]
        )
    if per_page < 1:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "per_page"],
                    "msg": "Input should be greater than or equal to 1",
                    "type": "value_error.number.not_ge"
                }
            ]
        )
    elif per_page > 20:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "per_page"],
                    "msg": "Input should be less than or equal to 20",
                    "type": "value_error.number.not_le"
                }
            ]
        )

    movies = await session.scalars(
        select(MovieModel)
        .offset((page - 1) * per_page)
        .limit(per_page)
        .order_by(MovieModel.id)
    )

    result = list(movies.all())
    if len(result) == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_items = await session.scalar(select(func.count()).select_from(MovieModel))
    total_pages = (total_items + per_page - 1) // per_page
    if page > 1:
        prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}"
    else:
        prev_page = None

    if page < total_pages:
        next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}"
    else:
        next_page = None

    return {
        "movies": result,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movies_by_id(movie_id: int, session: AsyncSession = Depends(get_db)):
    result = await session.scalar(select(MovieModel).where(MovieModel.id == movie_id))

    if result is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return result
