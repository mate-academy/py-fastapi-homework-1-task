from src.database.models import MovieModel
from src.database.session import get_db
from fastapi import APIRouter, Depends, HTTPException, Query
from src.schemas.movies import MovieDetailResponseSchema, MovieListResponseSchema
from sqlalchemy.orm import Session

router = APIRouter()



@router.get("/movies/", response_model=MovieListResponseSchema)
def get_movies(
        page: int = Query(default=1, ge=1, description="Номер страницы (>= 1)"),
        per_page: int = Query(default=10, ge=1, le=20, description="Количество фильмов на странице (>= 1 и <= 20)"),
        db: Session = Depends(get_db)
):
    # Подсчёт общего количества фильмов
    total_items = db.query(MovieModel).count()
    if total_items == 0:
        raise HTTPException(status_code=404, detail="No movies found.")

    # Вычисление начального индекса
    offset = (page - 1) * per_page

    # Получение фильмов с указанным смещением и лимитом
    movies = db.query(MovieModel).offset(offset).limit(per_page).all()

    base_url = "/movies/"
    prev_page = f"{base_url}?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"{base_url}?page={page + 1}&per_page={per_page}" if offset + per_page < total_items else None

    # Подготовка ответа
    return {
        "movies": movies,
        "prev_page": prev_page,
        "next_page": next_page,
        "total_pages": (total_items + per_page - 1) // per_page,
        "total_items": total_items,
    }


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
def get_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    # Поиск фильма по ID
    movie = db.query(MovieModel).filter(MovieModel.id == movie_id).first()
    if not movie:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")

    # Возврат данных фильма
    return movie
