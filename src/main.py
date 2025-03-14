import os
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db, close_db
from routes import movie_router

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

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

api_version_prefix = "/api/v1"

app.include_router(movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
app.include_router(movie_router, prefix=f"{api_version_prefix}/theater/movies", tags=["Movies"])
