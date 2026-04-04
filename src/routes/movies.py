from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.openapi.models import Response
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema
from database.crud import get_movie_list_with_limit_offset, get_movie_object

from database import get_db, MovieModel


router = APIRouter()
Page = Annotated[int, Query(ge=1)]
PerPage = Annotated[int, Query(ge=1, le=20)]
Database = Annotated[AsyncSession, Depends(get_db)]



@router.get("/movies", response_model=MovieListResponseSchema)
async def get_list_movies(
        request: Request,
        db: Database,
        page: Page = 1,
        per_page: PerPage = 10
):
    offset = (page - 1) * per_page
    limit = per_page

    result = (
        await get_movie_list_with_limit_offset(offset=offset, limit=limit, db=db)
    ).all()

    if result:
        movies = (elem[0] for elem in result)
        count = result[0][1]
        base_url = request.url.path
        return {
            "movies": movies,
            "prev_page": f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else "",
            "next_page": f"{base_url}?page={page + 1}&per_page={per_page}" if page < (pages := (count + per_page - 1) // per_page) else "",
            "total_items": count,
            "total_pages": pages,
        }
    raise HTTPException(status_code=404, detail="No movies found.")


@router.get("/movies/{movie_id}", response_model=MovieDetailResponseSchema)
async def get_movie_detail(db: Annotated[AsyncSession, Depends(get_db)], movie_id: int):
    movie = await get_movie_object(db=db, movie_id=movie_id)

    if not movie: raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return movie
