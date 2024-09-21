from dataclasses import dataclass

from core.abstract_dataclasses import AbstractDataclass
from core.clients.redis.models.trade_session.offer_type import OfferType


@dataclass
class OrderAction(AbstractDataclass):
    pass

    def get_offer_type(self) -> OfferType:
        if isinstance(self, CancelBuyAction):
            return OfferType.CANCEL_BUY
        if isinstance(self, CancelSellAction):
            return OfferType.CANCEL_SELL
        if isinstance(self, BuyAction):
            return OfferType.BUY
        if isinstance(self, SellAction):
            return OfferType.SELL
        raise Exception(f"Cannot transform order action of type {type(self).__name__} to OfferType")


@dataclass
class CancelOrderAction(OrderAction, AbstractDataclass):
    ge_slot: int


@dataclass
class InputOrderAction(OrderAction, AbstractDataclass):
    item_id: int
    item_name: str
    price: int
    quantity: int


@dataclass
class CancelBuyAction(CancelOrderAction):
    pass


@dataclass
class CancelSellAction(CancelOrderAction):
    pass


@dataclass
class BuyAction(InputOrderAction):
    pass


@dataclass
class SellAction(InputOrderAction):
    pass
