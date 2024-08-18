from clients.gds.models.config.strat_config import MMStratConfig, StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig
from strategy.exceptions import UnsupportedStratError
from strategy.mm import MMStrategy
from strategy.strategy import BaseStrategy


def provide_strategy(top_level_config: TopLevelConfig, strat_config: StratConfig) -> BaseStrategy:
    if isinstance(strat_config, MMStratConfig):
        return MMStrategy(top_level_config=top_level_config, strat_config=strat_config)
    raise UnsupportedStratError(type(strat_config).__name__)
