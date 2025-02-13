from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi_pagination import Page
from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi_pagination.ext.sqlalchemy import paginate as sqlalchemy_paginate, paginate
from starlette.responses import JSONResponse

from src.database.models import MovieModel
from src.database.session import get_db
from src.app import app
from src.schemas.movies import MovieBase, MovieDetailResponseSchema, MovieListResponseSchema


router = APIRouter()


@router.get("/movies/", response_model=MovieListResponseSchema)
def get_empty_movie(db: Session = Depends(get_db)):
    movies = db.query(MovieModel).all()
    return {"moviesssss": movies}

# @router.get(page: int = Query(1, ge=1), size: int = Query(10, ge=1))
# def get_empty_movie(page: int = , size db: Session = Depends(get_db)):
#     prev_page = page - 1
#     next_page = page + 1
#     total_pages = (total_items + size - 1) // size
#     total_items = db.query(MovieModel).count()
#     return JSONResponse(content={
#         "prev_page": prev_page,
#         "next_page": next_page,
#         "total_items": total_items,
#         'total_pages': total_pages,
#     })


@router.get("/movies/{film_id}", response_model=MovieDetailResponseSchema)
def get_movie_detail(film_id: int, db: Session = Depends(get_db)):
    film = db.query(MovieModel).filter(MovieModel.id == film_id).first()
    if not film:
        raise HTTPException(status_code=404, detail="Film not found")
    return film
