from dataclasses import dataclass
from enum import Enum, auto


class OrderType(Enum):

    NOT_SPECIFIED = auto()
    CANCEL = auto()
    BUY = auto()
    SELL = auto()

    @classmethod
    def from_str(cls, order_type: str) -> "OrderType":
        try:
            return cls[order_type.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED


@dataclass
class OrderMetadata:
    order_type: OrderType
    item_id: int
    price: int
    quantity: int
