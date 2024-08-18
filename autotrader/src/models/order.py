from dataclasses import dataclass

from utils.abstract_dataclasses import AbstractDataclass


@dataclass
class OrderAction(AbstractDataclass):
    name: str
    ge_slot: int


@dataclass
class InputOrder(OrderAction, AbstractDataclass):
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
