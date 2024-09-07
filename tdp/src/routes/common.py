import functools
from typing import Callable

from fastapi import HTTPException
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR


def handle_exceptions(f: Callable) -> Callable:
    @functools.wraps(f)
    async def wrapper(*args, **kwargs):
        try:
            return await f(*args, **kwargs)
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    return wrapper
