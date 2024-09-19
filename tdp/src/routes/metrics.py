from core.clients.redis.models.pnl.pnl import Pnl
from core.clients.tdp.stubs.metrics import GetNetWorthRequest, GetNetWorthResponse, GetPnlRequest, GetPnlResponse
from fastapi import APIRouter

from dependencies import MetricsCalculatorDep
from routes.common import handle_exceptions


router: APIRouter = APIRouter()


@router.get("/pnl", response_model=GetPnlResponse)
@handle_exceptions
async def get_pnl(
    metrics_calculator: MetricsCalculatorDep,
    request: GetPnlRequest,
) -> GetPnlResponse:
    pnl: Pnl = metrics_calculator.get_pnl(session_id=request.session_id)
    return GetPnlResponse(pnl=pnl)


@router.get("/nw", response_model=GetNetWorthResponse)
@handle_exceptions
async def get_nw(metrics_calculator: MetricsCalculatorDep, request: GetNetWorthRequest) -> GetNetWorthResponse:
    nw: int = metrics_calculator.get_nw(session_id=request.session_id)
    return GetNetWorthResponse(nw=nw)
