import logging
import time

from fastapi import status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from starlette.middleware.base import RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from app.main import app

# TODO: attach middlewares

logger = logging.getLogger(__name__)


async def add_ok_response(request: Request, call_next):
    response: Response = await call_next(request)
    if 200 <= response.status_code <= 299:
        pass


@app.middleware("http")
async def metrics_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    request_path = getattr(request, "path", request.url.path)
    path_template = ".".join(request_path.split("/")[1:])

    start_time = time.time()
    response = await call_next(request)
    elapsed_time = time.time() - start_time
    logger.debug(f"server.call.elapsed.{path_template}: {elapsed_time}")
    return response


@app.middleware("http")
async def exception_middleware(
    request: Request, call_next: RequestResponseEndpoint
) -> Response:
    try:
        response = await call_next(request)
    except ValidationError as e:
        logger.exception(e)
        response = JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"detail": e.errors()},
        )
    except ValueError as e:
        logger.exception(e)
        response = JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]
            },
        )
    except Exception as e:
        logger.exception(e)
        response = JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": [{"msg": "Unknown", "loc": ["Unknown"], "type": "Unknown"}]
            },
        )
    return response
