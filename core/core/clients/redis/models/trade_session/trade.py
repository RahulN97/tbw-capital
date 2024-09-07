from dataclasses import dataclass

from core.clients.redis.models.trade_session.order_metadata import OrderMetadata


@dataclass
class Trade:
    calc_cycle: int
    strat_name: str
    order_metadata: OrderMetadata
    time: float
