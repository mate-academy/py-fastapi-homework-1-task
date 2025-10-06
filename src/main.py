# src/main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from .database import init_db, close_db
from .routes import movie_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    try:
        yield
    finally:
        await close_db()


app = FastAPI(
    title="Movies homework",
    description="Description of project",
    lifespan=lifespan,
)

api_version_prefix = "/api/v1"
app.include_router(movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
