from fastapi_pagination import add_pagination

from src.routes.movies import router
from src.app import app


add_pagination(app)

api_version_prefix = "/api/v1"

app.include_router(router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
