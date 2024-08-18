from dataclasses import dataclass
from typing import List

from clients.gds.models.config.strat_config import StratConfig
from clients.gds.models.config.top_level_config import TopLevelConfig


@dataclass
class LiveConfig:
    trading_enabled: bool
    top_level_config: TopLevelConfig
    strat_configs: List[StratConfig]
