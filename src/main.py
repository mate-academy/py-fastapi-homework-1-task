from fastapi import FastAPI

from routes import movie_router
# from routes import movies

app = FastAPI(
    title="Movies homework",
    description="Description of project"
)

api_version_prefix = "/api/v1"

app.include_router(movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
# app.include_router(movies.router)
