from dataclasses import dataclass
from enum import Enum

from core.redis_object import RedisObject


class OrderType(Enum):

    NOT_SPECIFIED = "NOT_SPECIFIED"
    CANCEL = "CANCEL"
    BUY = "BUY"
    SELL = "SELL"

    @classmethod
    def from_str(cls, order_type: str) -> "OrderType":
        try:
            return cls[order_type.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED


@dataclass
class OrderMetadata(RedisObject):
    order_type: OrderType
    item_id: int
    price: int
    quantity: int
