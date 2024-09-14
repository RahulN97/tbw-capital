from dataclasses import dataclass
from typing import Dict, List

from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.config.environment import Environment
from core.redis_object import RedisObject


@dataclass
class TradeSession(RedisObject):
    session_id: str
    start_time: float
    start_nw: int
    env: Environment
    orders: Dict[str, List[Order]]
    trades: Dict[str, List[Trade]]
