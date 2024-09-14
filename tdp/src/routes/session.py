from collections import defaultdict
from typing import Any, Dict, List, Optional

from core.clients.redis.exceptions import RedisKeyError
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.tdp.stubs.session import (
    CreateTradeSessionRequest,
    GetOrdersRequest,
    GetOrdersResponse,
    GetTradeSessionRequest,
    GetTradeSessionResponse,
    GetTradesRequest,
    GetTradesResponse,
    UpdateOrdersRequest,
    UpdateTradesRequest,
    UpdateTradesResponse,
)
from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from dependencies import BookKeeperDep, RedisClientDep
from routes.common import handle_exceptions


router: APIRouter = APIRouter()


def filter_by_strats(vals: Dict[str, List[Any]], strats: Optional[List[str]]) -> Dict[str, List[Any]]:
    if strats is None:
        return vals
    return {s: v for s, v in vals.items() if s in strats}


@router.get("/", response_model=GetTradeSessionResponse)
@handle_exceptions
async def get_trade_session(
    redis_client: RedisClientDep,
    request: GetTradeSessionRequest = Body(...),
) -> GetTradeSessionResponse:
    try:
        trade_session: TradeSession = redis_client.get_trade_session(session_id=request.session_id)
        return GetTradeSessionResponse(trade_session=trade_session)
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Invalid session id. Make sure this trade session already exists. {str(e)}",
        )


@router.post("/")
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


@router.get("/orders", response_model=GetOrdersResponse)
@handle_exceptions
async def get_orders(redis_client: RedisClientDep, request: GetOrdersRequest = Body(...)) -> GetOrdersResponse:
    try:
        orders: Dict[str, List[Trade]] = redis_client.get_orders(session_id=request.session_id)
        return GetOrdersResponse(trades=filter_by_strats(vals=orders, strats=request.strats))
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Unable to fetch orders. Make sure trade session has already been saved. {str(e)}",
        )


@router.put("/orders")
@handle_exceptions
async def add_orders(book_keeper: BookKeeperDep, request: UpdateOrdersRequest) -> None:
    orders: Dict[str, List[Order]] = defaultdict(list)
    for order in request.orders:
        orders[order.strat_name].append(order)
    try:
        book_keeper.save_orders(session_id=request.session_id, orders=orders)
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Unable to save orders. Cannot append trades to a non-existent trade session. {str(e)}",
        )


@router.get("/trades", response_model=GetTradesResponse)
@handle_exceptions
async def get_trades(redis_client: RedisClientDep, request: GetTradesRequest = Body(...)) -> GetTradesResponse:
    try:
        trades: Dict[str, List[Trade]] = redis_client.get_trades(session_id=request.session_id)
        return GetTradesResponse(trades=filter_by_strats(vals=trades, strats=request.strats))
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Unable to fetch trades. Make sure trade session has already been saved. {str(e)}",
        )


@router.post("/trades", response_model=UpdateTradesResponse)
@handle_exceptions
async def add_trades(book_keeper: BookKeeperDep, request: UpdateTradesRequest) -> UpdateTradesResponse:
    try:
        trades: Dict[str, List[Trade]] = book_keeper.book_trades(
            session_id=request.session_id,
            calc_cycle=request.calc_cycle,
            cur_time=request.time,
        )
        return UpdateTradesResponse(trades=trades)
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Unable to book trades. Cannot append trades to a non-existent trade session. {str(e)}",
        )
