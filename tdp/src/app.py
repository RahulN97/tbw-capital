import uvicorn
from core.config.environment import Environment
from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from starlette.middleware.cors import CORSMiddleware
from uvicorn.main import ASGIApplication

from api import api_router
from config.tdp_config import TdpConfig
from dependencies import get_config
from handlers import log_stacktrace
from middleware import LogPerformanceMiddleware


def create_app() -> ASGIApplication:
    app: FastAPI = FastAPI(title="Trade Data Platform")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.add_middleware(LogPerformanceMiddleware)
    app.add_exception_handler(RequestValidationError, log_stacktrace)
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
