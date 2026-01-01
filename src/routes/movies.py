from fastapi import APIRouter, Depends, HTTPException, Query, Path
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.crud import get_movies_list, get_single_movie
from src.database.session import get_db
from src.schemas.movies import MoviesPageOut, MovieOut

movie_router = APIRouter(prefix="/movies", tags=["movies"])


@movie_router.get("/", response_model=MoviesPageOut)
async def list_movies(
    page: int = Query(1, ge=1),
    per_page: int = Query(10, ge=1, le=20),
    db: AsyncSession = Depends(get_db),
) -> MoviesPageOut:

    return await get_movies_list(page=page, per_page=per_page, db=db)


@movie_router.get("/{movie_id}/", response_model=MovieOut)
async def movie_details(
    movie_id: int = Path(..., ge=1),
    db: AsyncSession = Depends(get_db),
) -> MovieOut:
    movie = await get_single_movie(movie_id=movie_id, db=db)
    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
