from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from core.clients.gds.models.config.strat_config import StratConfig
from core.clients.gds.models.config.top_level_config import TopLevelConfig
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot import ExchangeSlot
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.price.models.item_metadata import ItemMetadata
from core.clients.price.models.price_data_snapshot import PriceDataSnapshot
from core.clients.redis.redis_client import RedisClient

from strategy.action import BuyAction, CancelOrderAction, OrderAction, SellAction
from strategy.constants import GP_ITEM_ID
from strategy.exceptions import MissingGpError


class BaseStrategy(ABC):

    def __init__(
        self,
        redis_client: RedisClient,
        top_level_config: TopLevelConfig,
        strat_config: StratConfig,
        universe: Optional[List[int]],
        item_map: Dict[int, ItemMetadata],
    ) -> None:
        self.redis_client: RedisClient = redis_client
        self.top_level_config: TopLevelConfig = top_level_config
        self.strat_config: StratConfig = strat_config
        self.universe: Optional[List[int]] = universe
        self.item_map: Dict[int, ItemMetadata] = (
            item_map if universe is None else {id: meta for id, meta in item_map.items() if id in universe}
        )
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
        cancels: List[CancelOrderAction],
        sells: List[SellAction],
        buys: List[BuyAction],
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
