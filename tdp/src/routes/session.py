from collections import defaultdict
from typing import Any, Dict, List, Optional

from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.redis.exceptions import RedisKeyError
from core.clients.redis.models.pnl.pnl import Pnl
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.start_metadata import StartMetadata
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.tdp.stubs.session import (
    CreateTradeSessionRequest,
    CreateTradeSessionResponse,
    CreateTradesRequest,
    CreateTradesResponse,
    GetOrdersRequest,
    GetOrdersResponse,
    GetTradeSessionRequest,
    GetTradeSessionResponse,
    GetTradesRequest,
    GetTradesResponse,
    UpdateOrdersRequest,
    UpdateTradeSessionRequest,
)
from core.config.environment import Environment
from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_404_NOT_FOUND, HTTP_409_CONFLICT

from dependencies import BookKeeperDep, GdsClientDep, MetricsCalculatorDep, RedisClientDep
from routes.common import handle_exceptions


router: APIRouter = APIRouter()


def filter_by_strats(vals: Dict[str, List[Any]], strats: Optional[List[str]]) -> Dict[str, List[Any]]:
    if strats is None:
        return vals
    return {s: v for s, v in vals.items() if s in strats}


def create_new_trade_session(
    session_id: str,
    player_name: str,
    env: Environment,
    start_time: float,
    start_nw: int,
    inv: Inventory,
) -> TradeSession:
    start_items: Dict[int, int] = defaultdict(int)
    for item in inv.items:
        start_items[item.id] += item.quantity

    start_metadata: StartMetadata = StartMetadata(start_time=start_time, start_nw=start_nw, start_items=start_items)

    return TradeSession(
        session_id=session_id,
        player_name=player_name,
        env=env,
        start_metadata=start_metadata,
        active_orders={},
        orders={},
        trades={},
    )


@router.get("", response_model=GetTradeSessionResponse)
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


@router.post("", response_model=CreateTradeSessionResponse)
@handle_exceptions
async def create_trade_session(
    redis_client: RedisClientDep,
    gds_client: GdsClientDep,
    metrics_calculator: MetricsCalculatorDep,
    request: CreateTradeSessionRequest,
) -> CreateTradeSessionResponse:
    try:
        redis_client.get_trade_session(session_id=request.session_id)
    except RedisKeyError:
        redis_client.set_session_validity(session_id=request.session_id, valid=True)

        pnl: Pnl = Pnl(
            session_id=request.session_id,
            total_pnl=0,
            pnl_snapshots=[],
            update_time=request.start_time,
        )
        redis_client.set_pnl_snapshot(session_id=request.session_id, pnl=pnl)

        trade_session: TradeSession = create_new_trade_session(
            session_id=request.session_id,
            player_name=request.player_name,
            env=request.env,
            start_time=request.start_time,
            start_nw=metrics_calculator.get_nw(session_id=request.session_id),
            inv=gds_client.get_inventory(),
        )
        redis_client.set_trade_session(trade_session=trade_session)

        return CreateTradeSessionResponse(trade_session=trade_session)
    else:
        raise HTTPException(
            status_code=HTTP_409_CONFLICT,
            detail=f"Trade session with id {request.session_id} already exists.",
        )


@router.put("")
@handle_exceptions
async def update_trade_session(redis_client: RedisClientDep, request: UpdateTradeSessionRequest) -> None:
    redis_client.set_trade_session(trade_session=request.trade_session)


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


@router.post("/trades", response_model=CreateTradesResponse)
@handle_exceptions
async def add_trades(book_keeper: BookKeeperDep, request: CreateTradesRequest) -> CreateTradesResponse:
    try:
        trades: Dict[str, List[Trade]] = book_keeper.book_trades(
            session_id=request.session_id,
            calc_cycle=request.calc_cycle,
            cur_time=request.time,
        )
        return CreateTradesResponse(trades=trades)
    except RedisKeyError as e:
        raise HTTPException(
            status_code=HTTP_404_NOT_FOUND,
            detail=f"Unable to book trades. Cannot append trades to a non-existent trade session. {str(e)}",
        )
