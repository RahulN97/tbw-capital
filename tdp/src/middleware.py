import time
from typing import Any, Callable

from core.logger import logger
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.types import ASGIApp


class LogPerformanceMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        super().__init__(app)

    async def dispatch(self, request: Request, call_next: Callable[..., Any]) -> Any:
        start_time: float = time.time()
        response: Any = await call_next(request)
        logger.info(f"Request processed in {time.time() - start_time:.4f} seconds")
        return response
