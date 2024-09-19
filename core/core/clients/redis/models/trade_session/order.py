from dataclasses import dataclass

from core.clients.redis.models.trade_session.offer_metadata import OfferMetadata
from core.redis_object import RedisObject


@dataclass
class Order(RedisObject):
    id: str
    calc_cycle: int
    strat_name: str
    metadata: OfferMetadata
    time: float
