from abc import ABC, abstractmethod
from typing import Dict, List, Optional

from clients.gds.models.config.strat_config import StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from clients.gds.models.exchange.exchange import Exchange
from clients.gds.models.inventory.inventory import Inventory
from clients.price.models.price_data_snapshot import PriceDataSnapshot
from models.order import OrderAction


class BaseStrategy(ABC):

    def __init__(
        self,
        top_level_config: TopLevelConfig,
        strat_config: StratConfig,
        universe: Optional[List[int]],
        item_map: Dict[int, str],
        f2p: bool,
    ) -> None:
        self.top_level_config: TopLevelConfig = top_level_config
        self.strat_config: StratConfig = strat_config
        self.universe: Optional[List[int]] = universe
        self.item_map: Dict[int, str] = (
            item_map if universe is None else {id: name for id, name in item_map.items() if id in universe}
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
