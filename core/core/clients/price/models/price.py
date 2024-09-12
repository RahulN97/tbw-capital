from dataclasses import dataclass

from core.abstract_dataclasses import AbstractDataclass
from core.clients.price.models.price_window import PriceWindow


@dataclass
class Price(AbstractDataclass):
    low_price: int
    high_price: int


@dataclass
class LatestPrice(Price):
    low_time: float
    high_time: float


@dataclass
class AvgPrice(Price):
    price_window: PriceWindow
    low_volume: int
    high_volume: int
    high_volume: int
