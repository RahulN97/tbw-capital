from typing import Dict, List, Optional

from pydantic import ConfigDict

from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.service import ApiBaseModel
from core.clients.tdp.models.item_container import ItemContainer


class GetBuyLimitsRequest(ApiBaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)
    container: ItemContainer
    item_ids: Optional[List[int]] = None


class GetBuyLimitsResponse(ApiBaseModel):
    buy_limits: Dict[int, BuyLimit]


class UpdateBuyLimitsRequest(ApiBaseModel):
    time: float
