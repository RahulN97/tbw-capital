from typing import Dict, List

from core.clients.redis.exceptions import RedisKeyError
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.tdp.stubs.trades import (
    CreateTradeSessionRequest,
    GetTradeSessionRequest,
    GetTradeSessionResponse,
    GetTradesRequest,
    GetTradesResponse,
    UpdateTradesRequest,
)
from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from dependencies import BookKeeperDep, RedisClientDep
from routes.common import handle_exceptions


router: APIRouter = APIRouter()


@router.get("/", response_model=GetTradesResponse)
@handle_exceptions
async def get_trades(redis_client: RedisClientDep, request: GetTradesRequest = Body(...)) -> GetTradesResponse:
    try:
        trades: Dict[str, List[Trade]] = redis_client.get_trades(session_id=request.session_id)
        if request.strats is not None:
            trades: Dict[str, List[Trade]] = {s: t for s, t in trades.items() if s in request.strats}
        return GetTradesResponse(trades=trades)
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Invalid session id. Make sure trade session has already been saved. {str(e)}",
        )


@router.put("/")
@handle_exceptions
async def add_trades(book_keeper: BookKeeperDep, request: UpdateTradesRequest) -> None:
    try:
        book_keeper.save_trades(session_id=request.session_id, strat_name=request.strat_name, trades=request.trades)
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Invalid session id. Cannot append trades to a non-existent trade session. {str(e)}",
        )


@router.get("/session", response_model=GetTradeSessionResponse)
@handle_exceptions
async def get_trade_session(
    redis_client: RedisClientDep,
    request: GetTradeSessionRequest = Body(...),
) -> GetTradeSessionResponse:
    try:
        return redis_client.get_trade_session(session_id=request.session_id)
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Invalid session id. Make sure this trade session already exists. {str(e)}",
        )


@router.post("/session")
@handle_exceptions
async def set_trade_session(
    redis_client: RedisClientDep,
    book_keeper: BookKeeperDep,
    request: CreateTradeSessionRequest,
) -> None:
    try:
        redis_client.get_trade_session(session_id=request.session_id)
    except RedisKeyError:
        book_keeper.save_trade_session(session=request.trade_session)
    else:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"Trade session with id {request.session_id} already exists.",
        )
