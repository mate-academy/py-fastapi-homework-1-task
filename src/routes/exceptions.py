from fastapi import HTTPException

from src.database import MovieModel


def validate_page(page: int):
    if page < 1:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "page"],
                    "msg": "ensure this value is greater than or equal to 1",
                    "type": "value_error.number.not_ge"
                }
            ]
        )


def validate_per_page(per_page: int):
    if not 1 <= per_page <= 20:
        raise HTTPException(
            status_code=422,
            detail=[
                {
                    "loc": ["query", "per_page"],
                    "msg": "ensure this value is greater than or equal to 1 "
                           "and less than or equal to 20",
                    "type": "value_error.number.not_ge"
                }
            ]
        )


def validate_movies_exist(movies: list[MovieModel] | None = None):
    if not movies:
        raise HTTPException(
            status_code=404,
            detail="No movies found."
        )
