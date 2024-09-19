import signal
import time
import types
from collections import defaultdict
from typing import Any, Callable, Dict, List, Optional

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.config.live_config import LiveConfig
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.gds.models.session_metadata import SessionMetadata
from core.clients.price.models.price_data_snapshot import PriceDataSnapshot
from core.clients.price.price_client import PriceClient
from core.clients.redis.models.trade_session.start_metadata import StartMetadata
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.redis.redis_client import RedisClient
from core.clients.tdp.tdp_client import TdpClient
from core.config.environment import Environment
from core.logger import logger

from executor import OrderExecutor
from interface.player import Player
from strategy.action import OrderAction
from strategy.strategy import BaseStrategy
from strategy.strategy_manager import StrategyManager


class Trader:

    def __init__(
        self,
        env: Environment,
        autotrader_wait: float,
        redis_client: RedisClient,
        price_client: PriceClient,
        gds_client: GdsClient,
        tdp_client: TdpClient,
        player: Player,
        order_executor: OrderExecutor,
        strat_manager: StrategyManager,
    ) -> None:
        self.env: Environment = env
        self.autotrader_wait: float = autotrader_wait
        self.redis_client: RedisClient = redis_client
        self.price_client: PriceClient = price_client
        self.gds_client: GdsClient = gds_client
        self.tdp_client: TdpClient = tdp_client
        self.player: Player = player
        self.order_executor: OrderExecutor = order_executor
        self.strat_manager: StrategyManager = strat_manager

        self._autotrader_active: bool = True
        self.session_metadata: SessionMetadata = gds_client.session_metadata
        self.trade_session: TradeSession = self.setup_trade_session()

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    @property
    def autotrader_active(self) -> bool:
        return self._autotrader_active

    @autotrader_active.setter
    def autotrader_active(self, val: bool) -> None:
        self._autotrader_active = val
        self.order_executor.abort = not val

    @staticmethod
    def lock_resources(f: Callable) -> Callable:
        def lock(self: "Trader", *args, **kwargs) -> Any:
            self.redis_client.set_session_validity(session_id=self.trade_session.session_id, valid=False)
            result: Any = f(self, *args, **kwargs)
            self.redis_client.set_session_validity(session_id=self.trade_session.session_id, valid=True)
            return result

        return lock

    def setup_trade_session(self) -> TradeSession:
        self.player.prepare()

        logger.info("Updating buy limits from last available GE snapshot")
        self.tdp_client.update_limits(
            player_name=self.session_metadata.player_name,
            cur_time=self.session_metadata.start_time,
        )

        logger.info("Liquidating and collecitng any remaining GE orders")
        self.order_executor.liquidate()

        logger.info(f"Setting up session {self.session_metadata.id} for player {self.session_metadata.player_name}")
        return self.tdp_client.create_trade_session(
            session_id=self.session_metadata.id,
            player_name=self.session_metadata.player_name,
            env=self.env,
            start_time=self.session_metadata.start_time,
        )

    def is_trading_enabled(self) -> bool:
        live_config: LiveConfig = self.gds_client.get_live_config()
        enabled: bool = live_config.trading_enabled
        logger.info(f"OSRS Trading is {'enabled' if enabled else 'disabled'}.")
        return enabled

    def wait(self, duration: Optional[float] = None) -> None:
        duration: float = duration or self.autotrader_wait
        logger.info(f"Waiting for {int(duration)} seconds until next trade loop")
        time.sleep(duration)

    @lock_resources
    def trade(self, calc_cycle: int, cur_time: float) -> None:
        logger.info(f"====== Trading enabled. Entering calc cycle {calc_cycle} ======")

        logger.info("Refreshing buy limits")
        self.tdp_client.update_limits(self.trade_session.player_name, cur_time)

        logger.info("Booking any completed trades in GE")
        self.order_executor.book_trades(calc_cycle, cur_time)

        logger.info("Fetching data snapshots required for strats")
        exchange: Exchange = self.gds_client.get_exchange()
        inventory: Inventory = self.gds_client.get_inventory()
        price_data: PriceDataSnapshot = self.price_client.get_price_data_snapshot()

        strats_to_compute: List[BaseStrategy] = self.strat_manager.prepare_strats(cur_time)
        logger.info(f"Prepared {len(strats_to_compute)} active strategies to compute")
        for strat in strats_to_compute:
            logger.info(f"--- Processing strat: {strat.name} ---")
            if strat.universe is not None:
                price_data: PriceDataSnapshot = PriceDataSnapshot.filter_by_items(
                    full_snapshot=price_data,
                    item_ids=strat.universe,
                )

            logger.info("Computing strat")
            actions: List[OrderAction] = strat.compute(
                exchange=exchange,
                inventory=inventory,
                price_data=price_data,
            )

            logger.info(f"Executing {len(actions)} order actions generated by strat")
            self.order_executor.execute(
                actions=actions,
                calc_cycle=calc_cycle,
                strat_name=strat.name,
            )

    def start(self) -> None:
        logger.info("Starting auto trader")

        calc_cycle: int = 0
        while self.autotrader_active:
            cur_time: float = time.time()

            if not self.is_trading_enabled():
                logger.info("Trading is not enabled")
                self.wait()
                continue

            self.player.prepare()

            calc_cycle += 1
            self.trade(calc_cycle, cur_time)

            duration: float = self.strat_manager.next_strat_wait_time(cur_time)
            self.wait(duration)

        logger.info("Exiting autotrader loop")

    def stop(self, signum: int, frame: Optional[types.FrameType]) -> None:
        logger.info(f"Received signal {signum}. Stopping auto trader")
        self.autotrader_active = False
        # TODO: save state of world, shutdown gracefully
