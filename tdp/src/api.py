from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from routes.limits import router as limits_router
from routes.pnl import router as pnl_router
from routes.session import router as session_router


api_router: APIRouter = APIRouter()
api_router.include_router(router=limits_router, prefix="/limits", tags=["limits"])
api_router.include_router(router=pnl_router, prefix="/pnl", tags=["pnl"])
api_router.include_router(router=session_router, prefix="/session", tags=["session"])


@api_router.get("/health", response_class=JSONResponse)
async def health() -> Dict[str, str]:
    return {"status": "healthy"}
