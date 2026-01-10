from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.session import get_db
from . import crud
from ..schemas.movies import MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", tags=["movies"], response_model=MovieListResponseSchema)
async def read_movies(
    db: AsyncSession = Depends(get_db), page: int = 1, per_page: int = 10
):
    result = await crud.get_movies(db=db, page=page, per_page=per_page)
    return result


@router.get("/movies/{movie_id}/", tags=["movies"])
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await crud.get_movie(movie_id=movie_id, db=db)
    if not result:
        raise HTTPException(
            status_code=404, detail="Movie with the given ID was not found."
        )
    return result
