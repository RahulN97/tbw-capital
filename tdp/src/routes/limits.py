from datetime import datetime
from typing import Dict

from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.tdp.models.item_container import ItemContainer
from core.clients.tdp.stubs.limits import GetBuyLimitsRequest, GetBuyLimitsResponse, UpdateBuyLimitsRequest
from core.logger import logger
from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from constants import GP_ITEM_ID
from dependencies import BookKeeperDep, GdsClientDep, RedisClientDep
from routes.common import handle_exceptions


router: APIRouter = APIRouter()


@router.get("/", response_model=GetBuyLimitsResponse)
@handle_exceptions
async def get_buy_limits(
    redis_client: RedisClientDep,
    gds_client: GdsClientDep,
    request: GetBuyLimitsRequest = Body(...),
) -> GetBuyLimitsResponse:
    logger.info(f"Attempting to fetch buy limits in container: {request.container.name}")
    buy_limits: Dict[int, BuyLimit] = {}
    if request.container == ItemContainer.EXCHANGE:
        exchange: Exchange = gds_client.get_exchange()
        for slot in exchange.slots:
            if slot.state == ExchangeSlotState.EMPTY or slot.item_id in buy_limits:
                continue
            buy_limits[slot.item_id] = redis_client.get_buy_limit(player_name=request.player_name, item_id=slot.item_id)
    elif request.container == ItemContainer.INVENTORY:
        inv: Inventory = gds_client.get_inventory()
        for item in inv.items:
            if item.id == GP_ITEM_ID or item.id in buy_limits:
                continue
            buy_limits[item.id] = redis_client.get_buy_limit(player_name=request.player_name, item_id=item.id)
    elif request.container == ItemContainer.ALL:
        buy_limits: Dict[int, BuyLimit] = redis_client.get_all_buy_limits(player_name=request.player_name)
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Cannot resolve item container: {request.container.name}",
        )

    if request.item_ids is not None:
        buy_limits: Dict[int, BuyLimit] = {id: bl for id, bl in buy_limits.items() if id in request.item_ids}

    return GetBuyLimitsResponse(buy_limits=buy_limits)


@router.post("/")
@handle_exceptions
async def update_buy_limits(book_keeper: BookKeeperDep, request: UpdateBuyLimitsRequest) -> None:
    update_time: float = request.time or datetime.now().timestamp()
    logger.info(f"Updating buy limits at time {update_time}")
    book_keeper.update_limits(player_name=request.player_name, cur_time=update_time)
