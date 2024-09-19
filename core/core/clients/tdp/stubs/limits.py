from typing import Dict, List, Optional

from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.service import ApiBaseModel
from core.clients.tdp.models.item_container import ItemContainer


class BuyLimitsRequest(ApiBaseModel):
    player_name: str


class GetBuyLimitsRequest(BuyLimitsRequest):
    container: ItemContainer
    item_ids: Optional[List[int]] = None


class GetBuyLimitsResponse(BuyLimitsRequest):
    buy_limits: Dict[int, BuyLimit]


class UpdateBuyLimitsRequest(BuyLimitsRequest):
    time: float
