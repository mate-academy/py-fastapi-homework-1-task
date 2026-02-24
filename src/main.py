from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.config import get_settings
from src.database import init_db, close_db
from src.routes.movies import router as movie_router


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

settings = get_settings()

app.include_router(
    movie_router,
    prefix=f"{settings.API_VERSION}{settings.THEATER_PREFIX}",
    tags=["theater"]
)
