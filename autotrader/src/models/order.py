from dataclasses import dataclass

from core.abstract_dataclasses import AbstractDataclass
from core.clients.redis.models.trade_session.offer_type import OfferType


@dataclass
class OrderAction(AbstractDataclass):
    pass

    def get_offer_type(self) -> OfferType:
        if isinstance(self, CancelOrder):
            return OfferType.CANCEL
        if isinstance(self, BuyOrder):
            return OfferType.BUY
        if isinstance(self, SellOrder):
            return OfferType.SELL
        raise Exception(f"Cannot transform order action of type {type(self).__name__} to OfferType")


@dataclass
class InputOrder(OrderAction, AbstractDataclass):
    item_id: int
    item_name: str
    price: int
    quantity: int


@dataclass
class CancelOrder(OrderAction):
    ge_slot: int


@dataclass
class BuyOrder(InputOrder):
    pass


@dataclass
class SellOrder(InputOrder):
    pass
