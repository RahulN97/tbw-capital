from typing import List, Optional

from pydantic import BaseModel

from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.tdp.models.item_container import ItemContainer


class GetBuyLimitsRequest(BaseModel):
    container: ItemContainer = ItemContainer.ALL
    item_ids: Optional[List[int]] = None


class GetBuyLimitsResponse(BaseModel):
    buy_limits: List[BuyLimit]


class UpdateBuyLimitsRequest(BaseModel):
    time: float
