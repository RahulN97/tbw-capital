from typing import List

from models.order import OrderAction
from strategy.strategy import BaseStrategy


class MMStrategy(BaseStrategy):

    def __init__(self, wait_duration: int, max_offer_time: int) -> None:
        super().__init__(wait_duration=wait_duration, max_offer_time=max_offer_time)

    @property
    def name(self) -> str:
        return "Market Maker"

    def compute(self) -> List[OrderAction]:
        return ["sleep"]
