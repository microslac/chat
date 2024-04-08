from typing import List, Optional
from fastapi import APIRouter
from starlette.responses import JSONResponse
from pydantic import BaseModel

from app.chat.routes.bot import router as bot_router
from app.chat.routes.chat import router as chat_router


class ErrorMessage(BaseModel):
    msg: str


class ErrorResponse(BaseModel):
    detail: Optional[List[ErrorMessage]]


api_router = APIRouter(
    default_response_class=JSONResponse,
    responses={
        400: {"model": ErrorResponse},
        401: {"model": ErrorResponse},
        403: {"model": ErrorResponse},
        404: {"model": ErrorResponse},
        500: {"model": ErrorResponse},
    },
)


@api_router.get("/healthcheck", include_in_schema=False)
def healthcheck():
    return {"ok": True}


api_router.include_router(bot_router, tags=["bot"])
api_router.include_router(chat_router, tags=["chat"])
