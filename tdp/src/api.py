from typing import Dict

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from routes.pnl import router as pnl_router
from routes.trades import router as trades_router


api_router: APIRouter = APIRouter()
api_router.include_router(pnl_router, prefix="/pnl", tags=["pnl"])
api_router.include_router(trades_router, prefix="/trades", tags=["trades"])


@api_router.get("/health", response_class=JSONResponse)
async def health() -> Dict[str, str]:
    return {"status": "healthy"}
