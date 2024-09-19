from dataclasses import dataclass

from core.clients.redis.models.trade_session.offer_type import OfferType
from core.redis_object import RedisObject


@dataclass
class OfferMetadata(RedisObject):
    type: OfferType
    item_id: int
    price: int
    quantity: int
    ge_slot: int
