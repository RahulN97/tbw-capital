from typing import Dict, List, Optional

from pydantic import ConfigDict

from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.service import ApiBaseModel


class TradeSessionRequest(ApiBaseModel):
    model_config = ConfigDict(use_enum_values=True, validate_default=True)
    session_id: str


# session #
class GetTradeSessionRequest(TradeSessionRequest):
    pass


class GetTradeSessionResponse(ApiBaseModel):
    trade_session: TradeSession


class CreateTradeSessionRequest(TradeSessionRequest):
    trade_session: TradeSession


# orders #
class GetOrdersRequest(TradeSessionRequest):
    strats: Optional[List[str]] = None


class GetOrdersResponse(ApiBaseModel):
    orders: Dict[str, List[Order]]


class UpdateOrdersRequest(TradeSessionRequest):
    orders: List[Order]


# trades #
class GetTradesRequest(TradeSessionRequest):
    strats: Optional[List[str]] = None


class GetTradesResponse(ApiBaseModel):
    trades: Dict[str, List[Trade]]


class UpdateTradesRequest(TradeSessionRequest):
    calc_cycle: int
    time: Optional[float] = None


class UpdateTradesResponse(ApiBaseModel):
    trades: Dict[str, List[Trade]]
