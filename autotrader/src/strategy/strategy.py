from abc import ABC, abstractmethod
from typing import List

from clients.gds.models.config.strat_config import StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from models.order import OrderAction


class BaseStrategy(ABC):

    def __init__(self, top_level_config: TopLevelConfig, strat_config: StratConfig) -> None:
        self.top_level_config: TopLevelConfig = top_level_config
        self.strat_config: StratConfig = strat_config

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @abstractmethod
    def compute(self) -> List[OrderAction]:
        pass
