from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db, MovieModel
from schemas.movies import MovieDetailResponseSchema, CustomMoviePagination

router = APIRouter()


@router.get("/movies/", response_model=CustomMoviePagination)
async def read_movies(
        request: Request,
        page: int = Query(1, ge=1, description="The page number to fetch."),
        per_page: int = Query(10, ge=1, le=20, description="Number of movies per page."),
        db: AsyncSession = Depends(get_db)
):
    count_query = select(func.count()).select_from(MovieModel)
    total_items = await db.scalar(count_query)

    if total_items == 0 or total_items is None:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page

    movie_query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(movie_query)
    movies = result.scalars().all()

    base_url = f"{request.url.scheme}://{request.url.netloc}{request.url.path}"

    prev_page = (
        f"{base_url}?page={page - 1}&per_page={per_page}"
        if page > 1 else None
    )
    next_page = (
        f"{base_url}?page={page + 1}&per_page={per_page}"
        if page < total_pages else None
    )

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def read_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    movie = await db.get(MovieModel, movie_id)

    if movie is None:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )
    return movie
