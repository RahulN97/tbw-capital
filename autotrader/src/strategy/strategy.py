from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from clients.gds.models.config.strat_config import StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from clients.gds.models.exchange.exchange import Exchange
from clients.gds.models.exchange.exchange_slot import ExchangeSlot
from clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from clients.gds.models.inventory.inventory import Inventory
from clients.price.models.item_metadata import ItemMetadata
from clients.price.models.price_data_snapshot import PriceDataSnapshot
from models.order import BuyOrder, CancelOrder, OrderAction, SellOrder
from strategy.constants import GP_ITEM_ID
from strategy.exceptions import MissingGpError


class BaseStrategy(ABC):

    def __init__(
        self,
        top_level_config: TopLevelConfig,
        strat_config: StratConfig,
        universe: Optional[List[int]],
        item_map: Dict[int, ItemMetadata],
        f2p: bool,
    ) -> None:
        self.top_level_config: TopLevelConfig = top_level_config
        self.strat_config: StratConfig = strat_config
        self.universe: Optional[List[int]] = universe
        self.item_map: Dict[int, ItemMetadata] = (
            item_map if universe is None else {id: meta for id, meta in item_map.items() if id in universe}
        )
        self.f2p: bool = f2p
        self.next_run_time: float = 0.0

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def compute(
        self,
        item_map: Dict[int, str],
        exchange: Exchange,
        inventory: Inventory,
        price_data: PriceDataSnapshot,
    ) -> List[OrderAction]:
        pass

    @staticmethod
    def get_gp(inventory: Inventory) -> int:
        for item in inventory.items:
            if item.id == GP_ITEM_ID:
                return item.quantity
        raise MissingGpError()

    def extract_executable_orders(
        self,
        exchange: Exchange,
        cancels: List[CancelOrder],
        sells: List[SellOrder],
        buys: List[BuyOrder],
    ) -> List[OrderAction]:
        available_slots: List[ExchangeSlot] = [s for s in exchange.slots if s.state == ExchangeSlotState.EMPTY]
        remaining_slots: int = len(available_slots) + len(cancels)
        if not remaining_slots:
            return cancels

        if remaining_slots - len(sells) <= 0:
            return cancels + sells[:remaining_slots]

        remaining_slots -= len(sells)
        return cancels + sells + buys[:remaining_slots]

    def validate_orders(self, orders: List[OrderAction]) -> None:
        pass
