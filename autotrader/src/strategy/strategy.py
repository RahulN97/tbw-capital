from abc import ABC, abstractmethod
from typing import List

from models.order import OrderAction


class BaseStrategy(ABC):

    def __init__(self, wait_duration: int, max_offer_time: int) -> None:
        self.wait_duration: int = wait_duration
        self.max_offer_time: int = max_offer_time

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def compute(self) -> List[OrderAction]:
        pass
