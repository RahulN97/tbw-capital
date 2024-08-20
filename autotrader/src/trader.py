import signal
import time
import types
from typing import Dict, List, Optional, Set

from clients.gds.gds_client import GdsClient
from clients.gds.models.config.live_config import LiveConfig
from clients.gds.models.exchange.exchange import Exchange
from clients.gds.models.inventory.inventory import Inventory
from clients.gds.models.player.camera import Camera
from clients.gds.models.player.player_location import PlayerLocation
from clients.gds.models.player.player_state import PlayerState
from clients.price.models.price_data_snapshot import PriceDataSnapshot
from clients.price.price_client import PriceClient
from exceptions import UnexpectedPlayerStateError, UnsupportedOrderActionError
from interface.controller import Controller
from models.order import BuyOrder, CancelOrder, InputOrder, OrderAction, SellOrder
from strategy.strategy import BaseStrategy
from strategy.strategy_factory import StrategyFactory
from utils.logging import logger


class Trader:

    EXPECTED_PLAYER_STATE: PlayerState = PlayerState(
        camera=Camera(z=-878, yaw=0, scale=3600),
        location=PlayerLocation(x=3165, y=3487),
    )

    def __init__(
        self,
        autotrader_wait: float,
        controller: Controller,
        price_client: PriceClient,
        gds_client: GdsClient,
        strat_factory: StrategyFactory,
    ) -> None:
        self.autotrader_wait: float = autotrader_wait
        self.controller: Controller = controller
        self.price_client: PriceClient = price_client
        self.gds_client: GdsClient = gds_client
        self.strat_factory: StrategyFactory = strat_factory

        self.autotrader_active: bool = True
        self.active_strats: Dict[str, BaseStrategy] = {}

        signal.signal(signal.SIGINT, self.stop)
        signal.signal(signal.SIGTERM, self.stop)

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
                self.active_strats[strat.name] = strat
            else:
                strat.top_level_config = live_config.top_level_config
                strat.strat_config = strat_config

            if cur_time < strat.next_run_time:
                continue

            strat.next_run_time = cur_time + strat_config.wait_duration
            strats_to_compute.append(strat)

        for strat_name in strats_to_remove:
            self.active_strats.pop(strat_name, None)

        return strats_to_compute

    def input_order(self, order: InputOrder) -> None:
        self.controller.click_location("ge_enter_quantity")
        self.controller.type(str(order.quantity))
        self.controller.press("enter")

        self.controller.click_location("ge_enter_price")
        self.controller.type(str(order.price))
        self.controller.press("enter")

        self.controller.click_location("ge_confirm")

    def process_actions(self, actions: List[OrderAction]) -> None:
        self.controller.open_ge()
        for action in actions:
            if not self.autotrader_active:
                raise Exception("Autotrader process terminated unexpectedly")
            if isinstance(action, CancelOrder):
                logger.info(f"Cancelling order in GE slot: {action.ge_slot} for item {action.name}")
                self.controller.click_ge_slot(action.ge_slot)
                self.controller.click_location("ge_abort_offer")
                self.controller.click_location("ge_back")
            elif isinstance(action, InputOrder):
                if isinstance(action, BuyOrder):
                    self.controller.click_ge_slot(action.ge_slot)
                    self.controller.type(action.name)
                    self.controller.press("enter")
                elif isinstance(action, SellOrder):
                    self.controller.click_inventory_slot(action.inventory_slot)
                else:
                    raise UnsupportedOrderActionError(
                        actual=type(action).__name__,
                        expected=InputOrder.__name__,
                    )
                submit_msg: str = f"Submitting {type(action).__name__} in GE slot: {action.ge_slot}"
                order_msg: str = f"item {action.name}, price: {action.price}, quantity: {action.quantity}"
                logger.info(f"{submit_msg} - {order_msg}")
                self.input_order(action)
            else:
                raise UnsupportedOrderActionError(
                    actual=type(action).__name__,
                    expected=OrderAction.__name__,
                )
            self.controller.click_location("ge_collect")
        self.controller.exit_ge()

    def wait(self, trading_enabled: bool, cur_time: float) -> None:
        if trading_enabled:
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

            logger.info("Fetching data snapshots required for strats")
            exchange: Exchange = self.gds_client.get_exchange()
            inventory: Inventory = self.gds_client.get_inventory()
            price_data: PriceDataSnapshot = self.price_client.get_price_data_snapshot()

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
                self.process_actions(actions)
                # TODO: save trades, update state of world

            self.wait(trading_enabled, cur_time)

        logger.info("Exiting autotrader loop")

    def stop(self, signum: int, frame: Optional[types.FrameType]) -> None:
        logger.info(f"Received signal {signum}. Stopping auto trader")
        self.autotrader_active = False
        # TODO: save state of world, shutdown gracefully
