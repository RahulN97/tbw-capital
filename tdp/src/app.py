import traceback

import uvicorn
from core.config.environment import Environment
from core.logger import logger
from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler
from starlette.middleware.cors import CORSMiddleware
from uvicorn.main import ASGIApplication

from api import api_router
from config.tdp_config import TdpConfig
from dependencies import get_config
from middleware import LogPerformanceMiddleware


def create_app() -> ASGIApplication:
    async def log_stacktrace(request: Request, exc: Exception) -> Response:
        msg: str = f"Error on request: {request.url}"
        logger.error(msg, exc_info=traceback.format_exc())
        return await http_exception_handler(request, exc)

    app: FastAPI = FastAPI(title="Trade Data Platform")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LogPerformanceMiddleware)
    app.add_exception_handler(HTTPException, log_stacktrace)
    app.include_router(api_router)
    return app


def start_server(app: ASGIApplication) -> None:
    config: TdpConfig = get_config()
    reload: bool = config.env == Environment.DEV
    app_target: ASGIApplication | str = "app:app" if reload or config.num_workers > 1 else app
    uvicorn.run(
        app_target,
        host=config.service_host,
        port=config.service_port,
        reload=reload,
        log_config=config.get_log_config(),
        log_level=config.log_level.lower(),
        workers=config.num_workers,
    )


app: ASGIApplication = create_app()
if __name__ == "__main__":
    start_server(app)
