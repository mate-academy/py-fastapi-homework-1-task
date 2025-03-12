from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db, MovieModel

router = APIRouter()


# @router.get("/movies/", response_model=MovieListResponseSchema)
# async def get_movies(
#         page: int,
#         per_page: int,
#         db: AsyncSession = Depends(get_db)
# ):
#     # Calculate offset for pagination
#     offset = (page - 1) * per_page
#
#     # Get total count of movies
#     count_query = select(func.count(MovieModel.id))
#     result = await db.execute(count_query)
#     total_items = result.scalar() or 0
#
#     # If no movies found, return 404
#     if total_items == 0:
#         raise HTTPException(status_code=404, detail="No movies found.")
#
#     # Calculate total pages
#     total_pages = ceil(total_items / per_page)
#
#     # Get movies for current page
#     query = select(MovieModel).offset(offset).limit(per_page)
#     result = await db.execute(query)
#     movies = result.scalars().all()
#
#     # Create pagination links - keep these as /theater/movies/ for consistency with example
#     base_url = "/theater/movies/"
#     prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
#     next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None
#
#     return MovieListResponseSchema(
#         movies=movies,
#         prev_page=prev_page,
#         next_page=next_page,
#         total_pages=total_pages,
#         total_items=total_items
#     )

@router.get("/movies/")
async def get_movies(
        db: AsyncSession = Depends(get_db),
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100)
):
    offset = (page - 1) * per_page
    query = select(MovieModel).offset(offset).limit(per_page)
    movies = await db.execute(query)
    movies_list = movies.scalars().all()

    total_items_query = select(MovieModel)
    total_items_result = await db.execute(total_items_query)
    total_items = len(total_items_result.scalars().all())

    if not movies_list:
        raise HTTPException(status_code=404, detail="No movies found.")

    total_pages = (total_items + per_page - 1) // per_page
    prev_page = page - 1 if page > 1 else None
    next_page = page + 1 if page < total_pages else None

    return {
        "movies": movies_list,
        "total_items": total_items,
        "total_pages": total_pages,
        "prev_page": prev_page,
        "next_page": next_page,
    }


@router.get("/movies/{movie_id}/")
async def get_movie_by_id(movie_id: int, db: AsyncSession = Depends(get_db)):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    return movie
