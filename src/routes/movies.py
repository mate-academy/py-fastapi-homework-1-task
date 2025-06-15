from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import JSONResponse

from database import get_db, MovieModel

from schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies(
        page: int = 1,
        per_page: int = 10,
        db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(func.count(MovieModel.id)))
    count_of_movies = result.scalar()
    if page <= 0 or per_page <= 0:
        return JSONResponse(
            status_code=422,
            content={"detail": [
                {"msg": "Input should be greater than or equal to 1"}
            ]
            }
        )

    total_pages = ((count_of_movies // per_page) +
                   (1 if count_of_movies % per_page != 0 else 0))

    if per_page > 20:
        return JSONResponse(
            status_code=422,
            content={"detail": [
                {"msg": "per page must be less than 20 and more than 0"}
            ]}
        )

    if page > total_pages:
        raise HTTPException(status_code=404, detail="No movies found.")

    offset = (page - 1) * per_page

    result = await db.execute(
        select(MovieModel).offset(offset).limit(per_page)
    )
    movies = result.scalars().all()

    if not movies:
        raise HTTPException(status_code=404, detail="No movies found")

    prev_page = None if page == 1 else \
        f"/theater/movies?page={page - 1}&per_page={per_page}"
    next_page = None if page == total_pages else \
        f"/theater/movies?page={page + 1}&per_page={per_page}"

    return {
        "movies": [
            {
                "id": movie.id, "name": movie.name,
                "date": movie.date, "score": movie.score,
                "genre": movie.genre, "overview": movie.overview,
                "crew": movie.crew, "orig_title": movie.orig_title,
                "status": movie.status, "orig_lang": movie.orig_lang,
                "budget": movie.budget, "revenue": movie.revenue,
                "country": movie.country
            } for movie in movies
        ],
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": total_pages,
        "total_items": count_of_movies
    }


@router.get(
    "/movies/{movie_id}/",
    response_model=MovieDetailResponseSchema
)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(MovieModel).where(MovieModel.id == movie_id)
    )
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=404,
            detail="Movie with the given ID was not found."
        )

    return movie
