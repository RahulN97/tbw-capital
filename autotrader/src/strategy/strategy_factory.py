import json
from typing import Dict, List

from clients.gds.models.config.strat_config import MMStratConfig, StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from strategy.exceptions import UnsupportedStratError
from strategy.mm import MMStrategy
from strategy.strategy import BaseStrategy


class StrategyFactory:

    def __init__(self) -> None:
        with open("data/universe.json", "r") as f:
            self.universe_map: Dict[str, List[int]] = json.load(f)

    def provide_strategy(self, top_level_config: TopLevelConfig, strat_config: StratConfig) -> BaseStrategy:
        if isinstance(strat_config, MMStratConfig):
            return MMStrategy(
                top_level_config=top_level_config,
                strat_config=strat_config,
                universe=self.universe_map.get(MMStrategy.__name__.lower()),
            )
        raise UnsupportedStratError(type(strat_config).__name__)
