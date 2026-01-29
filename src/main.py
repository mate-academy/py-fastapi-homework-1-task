from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import init_db, close_db
from routes import movies


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


app.include_router(movies.router, prefix=f"/theater", tags=["theater"])
