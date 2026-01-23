from src.schemas.movies import MovieListResponseSchema
from src.database import get_db

from fastapi import APIRouter, Depends, HTTPException, status, Request, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func

from src.database.models import MovieModel
from src.schemas import movies as schemas

router = APIRouter(
    prefix="/movies",
    tags=["Movies"]
)


@router.get("/", response_model=MovieListResponseSchema)
async def get_movies(
        request: Request,
        page: int = Query(1, ge=1),
        per_page: int = Query(10, ge=1, le=100),
        db: AsyncSession = Depends(get_db)
):
    offset = (page - 1) * per_page

    total_count_query = select(func.count()).select_from(MovieModel)
    total_count_result = await db.execute(total_count_query)
    total_items = total_count_result.scalar()

    query = select(MovieModel).offset(offset).limit(per_page)
    result = await db.execute(query)
    movies = result.scalars().all()

    total_pages = (total_items + per_page - 1) // per_page

    base_url = str(request.url).split('?')[0]

    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if page < total_pages else None

    return {
        "items": movies,
        "total_items": total_items,
        "total_pages": total_pages,
        "prev_page": prev_page,
        "next_page": next_page
    }


@router.post("/", response_model=schemas.MovieRead, status_code=status.HTTP_201_CREATED)
async def create_movie(
        movie: schemas.MovieCreate,
        db: AsyncSession = Depends(get_db)
):
    db_movie = MovieModel(**movie.model_dump())
    db.add(db_movie)
    try:
        await db.commit()
        await db.refresh(db_movie)
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Movie already exists or data is invalid"
        )
    return db_movie


@router.get("/{movie_id}", response_model=schemas.MovieDetailResponseSchema)
async def get_movie(
        movie_id: int,
        db: AsyncSession = Depends(get_db)
):
    query = select(MovieModel).where(MovieModel.id == movie_id)
    result = await db.execute(query)
    movie = result.scalar_one_or_none()

    if not movie:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Movie with the given ID was not found."
        )
    return movie
