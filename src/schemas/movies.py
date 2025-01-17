from pydantic import BaseModel
from typing import List, Optional


class MovieDetailResponseSchema(BaseModel):
    id: int
    name: str
    date: str
    score: Optional[float]
    genre: Optional[str]
    overview: Optional[str]
    crew: Optional[str]
    orig_title: Optional[str]
    status: Optional[str]
    orig_lang: Optional[str]
    budget: Optional[int]
    revenue: Optional[int]
    country: Optional[str]

    class Config:
        orm_mode = True  # Для интеграции с SQLAlchemy ORM


class MovieListResponseSchema(BaseModel):
    movies: List[MovieDetailResponseSchema]  # Список фильмов
    prev_page: Optional[str]  # URL на предыдущую страницу
    next_page: Optional[str]  # URL на следующую страницу
    total_pages: int  # Общее количество страниц
    total_items: int  # Общее количество элементов

