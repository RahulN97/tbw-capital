import json
from typing import Dict, List

from core.clients.redis.redis_client import RedisClient

from clients.gds.models.config.strat_config import MMStratConfig, StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from clients.price.models.item_metadata import ItemMetadata
from clients.price.price_client import PriceClient
from strategy.exceptions import UnsupportedStratError
from strategy.mm import MMStrategy
from strategy.strategy import BaseStrategy


class StrategyFactory:

    def __init__(self, redis_client: RedisClient, price_client: PriceClient, is_f2p: bool) -> None:
        self.redis_client: RedisClient = redis_client
        self.item_map: Dict[int, ItemMetadata] = price_client.get_item_mapping()
        self.universe_map: Dict[str, List[int]] = self.get_universe_map(is_f2p)

    def get_universe_map(self, is_f2p: bool) -> Dict[str, List[int]]:
        with open("data/universe.json", "r") as f:
            universe_map: Dict[str, List[int]] = json.load(f)
        if not is_f2p:
            return universe_map
        return {
            strat: [u for u in universe if not self.item_map[u].members] for strat, universe in universe_map.items()
        }

    def provide_strategy(self, top_level_config: TopLevelConfig, strat_config: StratConfig) -> BaseStrategy:
        if isinstance(strat_config, MMStratConfig):
            return MMStrategy(
                redis_client=self.redis_client,
                top_level_config=top_level_config,
                strat_config=strat_config,
                universe=self.universe_map.get(MMStrategy.__name__.lower()),
                item_map=self.item_map.copy(),
            )
        raise UnsupportedStratError(type(strat_config).__name__)
        raise UnsupportedStratError(type(strat_config).__name__)
