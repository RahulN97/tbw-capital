import json
from typing import Dict, List

from clients.gds.models.config.strat_config import MMStratConfig, StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from clients.price.price_client import PriceClient
from strategy.exceptions import UnsupportedStratError
from strategy.mm import MMStrategy
from strategy.strategy import BaseStrategy


class StrategyFactory:

    def __init__(self, price_client: PriceClient) -> None:
        self.item_map: Dict[int, str] = price_client.get_item_mapping()
        with open("data/universe.json", "r") as f:
            self.universe_map: Dict[str, List[int]] = json.load(f)

    def provide_strategy(self, top_level_config: TopLevelConfig, strat_config: StratConfig, f2p: bool) -> BaseStrategy:
        if isinstance(strat_config, MMStratConfig):
            return MMStrategy(
                top_level_config=top_level_config,
                strat_config=strat_config,
                universe=self.universe_map.get(MMStrategy.__name__.lower()),
                item_map=self.item_map.copy(),
                f2p=f2p,
            )
        raise UnsupportedStratError(type(strat_config).__name__)
