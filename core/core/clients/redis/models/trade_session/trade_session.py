from dataclasses import dataclass
from typing import List

from core.clients.redis.models.trade_session.trade import Trade


@dataclass
class TradeSession:
    session_id: str
    start_time: float
    is_dev: bool
    trades: List[Trade]
