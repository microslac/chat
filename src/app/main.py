import uvicorn
from fastapi import FastAPI
from langserve import add_routes
from fastapi.middleware.cors import CORSMiddleware

from app.api import api_router
from app.exceptions import exception_handlers, limiter
from app.chat.llms import llama, phi
from app.chat.serve.chain import create_chain, per_req_config_modifier
from app.lifespan import lifespan
from app.settings import settings
from app.database import create_all

create_all()

app = FastAPI(
    title="chat",
    description="chat",
    exception_handlers=exception_handlers,
    lifespan=lifespan,
    limiter=limiter,
)

add_routes(
    app,
    create_chain(llama.chain),
    per_req_config_modifier=per_req_config_modifier,
    path="/chat",
)

add_routes(
    app,
    create_chain(phi.chain),
    per_req_config_modifier=per_req_config_modifier,
    path="/phi",
)

# TODO: middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=settings.cors.allow_credentials,
    allow_origins=settings.cors.allow_origins,
    allow_headers=settings.cors.allow_headers,
    allow_methods=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    uvicorn.run("main:app", host=settings.api.host, port=settings.api.port, reload=True)
