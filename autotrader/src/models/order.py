from dataclasses import dataclass

from utils.abstract_dataclasses import AbstractDataclass


@dataclass
class OrderAction(AbstractDataclass):
    ge_slot: int


@dataclass
class InputOrder(AbstractDataclass, OrderAction):
    name: str
    price: int
    quantity: int


@dataclass
class CancelOrder(OrderAction):
    pass


@dataclass
class BuyOrder(InputOrder):
    pass


@dataclass
class SellOrder(InputOrder):
    inventory_slot: int
