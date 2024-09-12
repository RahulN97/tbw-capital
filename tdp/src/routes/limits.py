from datetime import datetime
from typing import List

from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.tdp.models.item_container import ItemContainer
from core.clients.tdp.stubs.buy_limit import GetBuyLimitsRequest, GetBuyLimitsResponse, UpdateBuyLimitsRequest
from core.logger import logger
from fastapi import APIRouter, Body, HTTPException
from starlette.status import HTTP_400_BAD_REQUEST

from dependencies import BookKeeperDep, GdsClientDep, RedisClientDep
from routes.common import handle_exceptions
from routes.constants import GP_ITEM_ID


router: APIRouter = APIRouter()


@router.get("/", response_model=GetBuyLimitsResponse)
@handle_exceptions
async def get_buy_limits(
    redis_client: RedisClientDep,
    gds_client: GdsClientDep,
    request: GetBuyLimitsRequest = Body(...),
) -> GetBuyLimitsResponse:
    logger.info(f"Attempting to fetch buy limits in container: {request.container.name}")
    if request.container == ItemContainer.EXCHANGE:
        exchange: Exchange = gds_client.get_exchange()
        buy_limits: List[BuyLimit] = [
            redis_client.get_buy_limit(slot.item_id) for slot in exchange.slots if slot.state != ExchangeSlotState.EMPTY
        ]
    elif request.container == ItemContainer.INVENTORY:
        inv: Inventory = gds_client.get_inventory()
        buy_limits: List[BuyLimit] = [
            redis_client.get_buy_limit(item.id) for item in inv.items if item.id != GP_ITEM_ID
        ]
    elif request.container == ItemContainer.ALL:
        buy_limits: List[BuyLimit] = list(redis_client.get_all_buy_limits())
    else:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=f"Cannot resolve item container: {request.container.name}",
        )

    if request.item_ids is not None:
        buy_limits: List[BuyLimit] = [bl for bl in buy_limits if bl.item_id in request.item_ids]

    return GetBuyLimitsResponse(buy_limits=buy_limits)


@router.post("/")
@handle_exceptions
async def update_buy_limits(book_keeper: BookKeeperDep, request: UpdateBuyLimitsRequest) -> None:
    update_time: float = request.time or datetime.now().timestamp()
    logger.info(f"Updating buy limits at time {update_time}")
    book_keeper.update_limits(cur_time=update_time)
