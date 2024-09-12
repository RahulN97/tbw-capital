from dataclasses import dataclass
from typing import Dict, List

from core.clients.redis.models.trade_session.trade import Trade
from core.redis_object import RedisObject


@dataclass
class TradeSession(RedisObject):
    session_id: str
    start_time: float
    is_dev: bool
    trades: Dict[str, List[Trade]]
