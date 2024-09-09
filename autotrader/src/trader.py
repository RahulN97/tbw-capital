import signal
import time
import types
from typing import Dict, List, Optional, Set

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.config.live_config import LiveConfig
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.gds.models.player.camera import Camera
from core.clients.gds.models.player.player_location import PlayerLocation
from core.clients.gds.models.player.player_state import PlayerState
from core.clients.gds.models.session_metadata import SessionMetadata
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.config.environment import Environment
from core.logger import logger
from core.tracking.book_keeper import BookKeeper

from clients.price.models.item_metadata import ItemMetadata
from clients.price.models.price_data_snapshot import PriceDataSnapshot
from clients.price.price_client import PriceClient
from exceptions import UnexpectedPlayerStateError
from executor import OrderExecutor
from interface.controller import Controller
from models.order import OrderAction
from strategy.strategy import BaseStrategy
from strategy.strategy_factory import StrategyFactory


class Trader:

    EXPECTED_PLAYER_STATE: PlayerState = PlayerState(
        camera=Camera(z=-878, yaw=0, scale=3600),
        location=PlayerLocation(x=3165, y=3487),
    )

    def __init__(
        self,
        env: Environment,
        autotrader_wait: float,
        controller: Controller,
        order_executor: OrderExecutor,
        price_client: PriceClient,
        gds_client: GdsClient,
        strat_factory: StrategyFactory,
        book_keeper: BookKeeper,
    ) -> None:
        self.env: Environment = env
        self.autotrader_wait: float = autotrader_wait
        self.controller: Controller = controller
        self.order_executor: OrderExecutor = order_executor
        self.price_client: PriceClient = price_client
        self.gds_client: GdsClient = gds_client
        self.strat_factory: StrategyFactory = strat_factory
        self.book_keeper: BookKeeper = book_keeper

        self._autotrader_active: bool = True
        self.active_strats: Dict[str, BaseStrategy] = {}
        self.calc_cycle: int = 0
        self.item_map: Dict[int, ItemMetadata] = price_client.item_map
        self.trade_session: TradeSession = self.create_trade_session()

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

    @property
    def autotrader_active(self) -> bool:
        return self._autotrader_active

    @autotrader_active.setter
    def autotrader_active(self, val: bool) -> None:
        self._autotrader_active = val
        self.order_executor.abort = not val

    def create_trade_session(self) -> TradeSession:
        session: SessionMetadata = self.gds_client.get_session_metadata()
        trade_session: TradeSession = TradeSession(
            session_id=session.id,
            start_time=session.start_time,
            is_dev=self.env == Environment.DEV,
            trades=[],
        )
        self.book_keeper.save_trade_session(trade_session)
        return trade_session

    def is_trading_enabled(self) -> bool:
        live_config: LiveConfig = self.gds_client.get_live_config()
        enabled: bool = live_config.trading_enabled
        logger.info(f"OSRS Trading is {'enabled' if enabled else 'disabled'}.")
        return enabled

    def is_player_ready(self) -> bool:
        player_state: PlayerState = self.gds_client.get_player_data()
        return (
            player_state.location == self.EXPECTED_PLAYER_STATE.location
            and player_state.camera.z == self.EXPECTED_PLAYER_STATE.camera.z
            and player_state.camera.yaw == self.EXPECTED_PLAYER_STATE.camera.yaw
            and player_state.camera.scale > self.EXPECTED_PLAYER_STATE.camera.scale
        )

    def prepare_player(self) -> None:
        self.controller.click_location("compass")
        # TODO: walk to ge tile if needed
        self.controller.scroll_full_zoom()
        self.controller.hold("down", 3)
        if not self.is_player_ready():
            player_state: PlayerState = self.gds_client.get_player_data()
            raise UnexpectedPlayerStateError(
                player_state=player_state,
                expected_player_state=self.EXPECTED_PLAYER_STATE,
            )

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

    def wait(self, trading_enabled: bool, cur_time: float) -> None:
        if trading_enabled and self.active_strats:
            strat_run_times: List[float] = [s.next_run_time for s in self.active_strats.values()]
            next_run_time: float = min(strat_run_times, default=cur_time + 1)
            wait_time: float = max(next_run_time - cur_time, 0.0)
        else:
            wait_time: float = self.autotrader_wait

        logger.info(f"Waiting for {int(wait_time)} seconds until next trade loop")
        time.sleep(wait_time)

    def start(self) -> None:
        logger.info("Starting auto trader")

        while self.autotrader_active:
            cur_time: float = time.time()

            if not (trading_enabled := self.is_trading_enabled()):
                self.wait(trading_enabled, cur_time)
                continue

            if not self.is_player_ready():
                logger.info("Preparing player at exchange")
                self.prepare_player()

            self.calc_cycle += 1

            logger.info("Fetching data snapshots required for strats")
            exchange: Exchange = self.gds_client.get_exchange()
            inventory: Inventory = self.gds_client.get_inventory()
            price_data: PriceDataSnapshot = self.price_client.get_price_data_snapshot()

            logger.info("Refreshing buy limits")
            self.book_keeper.update_limits(cur_time)

            logger.info("Preparing strategies")
            strats_to_compute: List[BaseStrategy] = self.prepare_strats(cur_time)
            for strat in strats_to_compute:
                if strat.universe is not None:
                    price_data: PriceDataSnapshot = PriceDataSnapshot.filter_by_items(
                        full_snapshot=price_data,
                        item_ids=strat.universe,
                    )

                logger.info(f"Computing strat: {strat.name}")
                actions: List[OrderAction] = strat.compute(
                    exchange=exchange,
                    inventory=inventory,
                    price_data=price_data,
                )

                logger.info(f"Processing order actions for strat: {strat.name}")
                self.order_executor.execute(actions)

                logger.info(f"Saving trades for strategy {strat.name}")
                self.book_keeper.save_trades(actions, strat.name)

            self.wait(trading_enabled, cur_time)

        logger.info("Exiting autotrader loop")

    def stop(self, signum: int, frame: Optional[types.FrameType]) -> None:
        logger.info(f"Received signal {signum}. Stopping auto trader")
        self.autotrader_active = False
        # TODO: save state of world, shutdown gracefully
