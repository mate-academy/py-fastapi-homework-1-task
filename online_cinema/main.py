from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import users, movies
from database import engine
from models import Base

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(users.router)
app.include_router(movies.router)
