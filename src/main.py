from fastapi_pagination import add_pagination

from src.app import app
from src.routes.movies import router


# add_pagination(app)

api_version_prefix = "/api/v1"

app.include_router(router, prefix=f"{api_version_prefix}/theater", tags=["theater"])
