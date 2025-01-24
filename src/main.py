from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from routes import movie_router

app = FastAPI(
    title="Movies homework",
    description="Description of project"
)

api_version_prefix = "/api/v1"

app.include_router(movie_router, prefix=f"{api_version_prefix}/theater", tags=["theater"])


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        errors.append({
            "loc": err["loc"],
            "msg": "ensure this value is greater than or equal to 1"
            if "greater_than_equal" in err["type"] else err["msg"],
            "type": "value_error.number.not_ge"
            if "greater_than_equal" in err["type"] else err["type"]
        })
    return JSONResponse(
        status_code=422,
        content={"detail": errors}
    )
