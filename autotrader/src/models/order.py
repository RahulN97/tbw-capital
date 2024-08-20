from dataclasses import dataclass

from utils.abstract_dataclasses import AbstractDataclass


@dataclass
class OrderAction(AbstractDataclass):
    pass


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
