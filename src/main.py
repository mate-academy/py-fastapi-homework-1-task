from fastapi import FastAPI
from fastapi_pagination import add_pagination

from src.routes import movie_router

app = FastAPI(
    title="Movies homework",
    description="Description of project"
)
add_pagination(app)

api_version_prefix = "/api/v1"


app.include_router(movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
