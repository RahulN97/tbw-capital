from typing import Dict, List, Optional

from pydantic import BaseModel

from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession


class TradeRequest(BaseModel):
    session_id: str


class GetTradeSessionRequest(TradeRequest):
    pass


class GetTradeSessionResponse(BaseModel):
    trade_session: TradeSession


class CreateTradeSessionRequest(TradeRequest):
    trade_session: TradeSession


class GetTradesRequest(TradeRequest):
    strats: Optional[List[str]] = None


class GetTradesResponse(BaseModel):
    trades: Dict[str, List[Trade]]


class UpdateTradesRequest(TradeRequest):
    strat_name: str
    trades: List[Trade]
