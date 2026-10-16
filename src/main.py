from contextlib import asynccontextmanager
from typing import Generator

from fastapi import FastAPI, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session

from database.models import MovieModel
from schemas.movies import MovieDetailResponseSchema
from database import init_db, close_db, get_db
from routes import movie_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Movies homework",
    description="Description of project",
    lifespan=lifespan
)

@app.get("/movies/", response_model=list[MovieDetailResponseSchema])
async def get_all_movies(db: AsyncSession = Depends(get_db)):
    result = await db.scalars(select(MovieModel))
    return result.all()



api_version_prefix = "/api/v1"

app.include_router(movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
