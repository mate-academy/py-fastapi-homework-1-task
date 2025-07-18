from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware import Middleware

from database import init_db, close_db
from middlewares.pagination import PaginationMiddleware
from routes import movie_router


middleware = [Middleware(PaginationMiddleware)]


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()


app = FastAPI(
    title="Movies homework",
    description="Description of project",
    lifespan=lifespan,
    middleware=middleware,
)

api_version_prefix = "/api/v1"

app.include_router(
    movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"]
)
