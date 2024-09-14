import traceback
from typing import Union

from core.logger import logger
from fastapi import HTTPException, Request, Response
from fastapi.exception_handlers import http_exception_handler, request_validation_exception_handler
from fastapi.exceptions import RequestValidationError
from starlette.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


async def log_stacktrace(request: Request, exc: Union[RequestValidationError | HTTPException]) -> Response:
    msg: str = f"Error on request: {request.url}"
    logger.error(msg, exc_info=traceback.format_exc())

    if isinstance(exc, RequestValidationError):
        return await request_validation_exception_handler(request, exc)
    if isinstance(exc, HTTPException):
        return await http_exception_handler(request, exc)
    return JSONResponse(status_code=HTTP_500_INTERNAL_SERVER_ERROR, content={"detail": str(exc)})
