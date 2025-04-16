from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel
from schemas import MovieListResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema, responses={
    404: {
        "description": "No movies found.",
        "content": {
            "application/json": {
                "example": {"detail": "No movies found."}
            }
        }
    }
})
async def get_movies(
    page: Annotated[
        int, Query(ge=1, description="The page number to fetch")
    ] = 1,
    per_page: Annotated[int, Query(
        ge=1, le=20, description="Number of movies to fetch per page"
    )] = 10,
    db: AsyncSession = Depends(get_db)
):
    count_query = select(func.count()).select_from(MovieModel)
    count_result = await db.execute(count_query)
    total_items = count_result.scalar()

    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page
    total_pages = (total_items + per_page - 1) // per_page

    query = select(MovieModel).limit(per_page).offset(offset)
    result = await db.execute(query)
    movies = result.scalars().all()

    prev_page = f"/theater/movies/?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/theater/movies/?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": total_items,
    }
