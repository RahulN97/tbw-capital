import time
from typing import Dict, List, Optional, Set

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.config.live_config import LiveConfig
from core.logger import logger

from strategy.strategy import BaseStrategy
from strategy.strategy_factory import StrategyFactory


class StrategyManager:

    def __init__(self, strat_factory: StrategyFactory, gds_client: GdsClient) -> None:
        self.strat_factory: StrategyFactory = strat_factory
        self.gds_client: GdsClient = gds_client
        self.active_strats: Dict[str, BaseStrategy] = {}

    def prepare_strats(self, cur_time: float) -> None:
        live_config: LiveConfig = self.gds_client.get_live_config()

        strats_to_remove: Set[str] = set()
        strats_to_compute: List[BaseStrategy] = []

        for strat_config in live_config.strat_configs:
            if not strat_config.activated:
                strats_to_remove.add(strat_config.strat_name)
                continue

            strat: Optional[BaseStrategy] = self.active_strats.get(strat_config.strat_name)
            if strat is None:
                strat = self.strat_factory.provide_strategy(
                    top_level_config=live_config.top_level_config,
                    strat_config=strat_config,
                )
                self.active_strats[strat_config.strat_name] = strat
            else:
                strat.top_level_config = live_config.top_level_config
                strat.strat_config = strat_config

            if cur_time < strat.next_run_time:
                continue

            strat.next_run_time = cur_time + strat_config.wait_duration
            strats_to_compute.append(strat)

        for strat_name in strats_to_remove:
            logger.info(f"Deactivated {strat_name}. Removing it from active strats")
            self.active_strats.pop(strat_name, None)

        return strats_to_compute

    def next_strat_wait_time(self, cur_time: float) -> Optional[float]:
        if not self.active_strats:
            return

        strat_run_times: List[float] = [s.next_run_time for s in self.active_strats.values()]
        next_run_time: float = min(strat_run_times, default=cur_time + 1)
        return max(next_run_time - cur_time, 0.0)
