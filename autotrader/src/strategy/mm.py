from typing import List

from clients.gds.models.config.strat_config import MMStratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from clients.gds.models.exchange.exchange import Exchange
from clients.gds.models.inventory.inventory import Inventory
from models.order import BuyOrder, CancelOrder, OrderAction, SellOrder
from strategy.strategy import BaseStrategy


class MMStrategy(BaseStrategy):

    def __init__(self, top_level_config: TopLevelConfig, strat_config: MMStratConfig) -> None:
        super().__init__(top_level_config=top_level_config, strat_config=strat_config)

    @property
    def name(self) -> str:
        return "Market Maker"

    def compute(self, exchange: Exchange, inventory: Inventory) -> List[OrderAction]:
        # for demo
        return [
            BuyOrder(ge_slot=0, name="nature rune", price=150, quantity=10),
            SellOrder(ge_slot=0, name="nature rune", price=160, quantity=5, inventory_slot=4),
            CancelOrder(ge_slot=0, name="nature rune"),
            SellOrder(ge_slot=0, name="nature rune", price=100, quantity=10, inventory_slot=4),
        ]
