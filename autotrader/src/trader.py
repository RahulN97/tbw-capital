import signal
import time
import types
from typing import List, Optional

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.config.live_config import LiveConfig
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.gds.models.session_metadata import SessionMetadata
from core.clients.price.models.price_data_snapshot import PriceDataSnapshot
from core.clients.price.price_client import PriceClient
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.tdp.tdp_client import TdpClient
from core.config.environment import Environment
from core.logger import logger

from executor import OrderExecutor
from interface.player import Player
from models.order import OrderAction
from strategy.strategy import BaseStrategy
from strategy.strategy_manager import StrategyManager


class Trader:

    def __init__(
        self,
        env: Environment,
        autotrader_wait: float,
        price_client: PriceClient,
        gds_client: GdsClient,
        tdp_client: TdpClient,
        player: Player,
        order_executor: OrderExecutor,
        strat_manager: StrategyManager,
    ) -> None:
        self.env: Environment = env
        self.autotrader_wait: float = autotrader_wait
        self.price_client: PriceClient = price_client
        self.gds_client: GdsClient = gds_client
        self.tdp_client: TdpClient = tdp_client
        self.player: Player = player
        self.order_executor: OrderExecutor = order_executor
        self.strat_manager: StrategyManager = strat_manager

        self._autotrader_active: bool = True
        self.calc_cycle: int = 0
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
            start_nw=0,  # tdp_client.get_nw()
            env=self.env,
            orders={},
            trades={},
        )
        self.tdp_client.save_trade_session(trade_session)
        return trade_session

    def is_trading_enabled(self) -> bool:
        live_config: LiveConfig = self.gds_client.get_live_config()
        enabled: bool = live_config.trading_enabled
        logger.info(f"OSRS Trading is {'enabled' if enabled else 'disabled'}.")
        return enabled

    def wait(self, duration: Optional[float] = None) -> None:
        duration: float = duration or self.autotrader_wait
        logger.info(f"Waiting for {int(duration)} seconds until next trade loop")
        time.sleep(duration)

    def start(self) -> None:
        logger.info("Starting auto trader")

        while self.autotrader_active:
            cur_time: float = time.time()

            if not self.is_trading_enabled():
                logger.info("Trading is not enabled")
                self.wait()
                continue

            self.player.prepare()

            self.calc_cycle += 1
            logger.info(f"Trading enabled. Entering calc cycle {self.calc_cycle}")

            logger.info("Booking any completed trades in GE")
            self.tdp_client.book_trades(
                session_id=self.trade_session.session_id,
                calc_cycle=self.calc_cycle,
                time=cur_time,
            )

            logger.info("Fetching data snapshots required for strats")
            exchange: Exchange = self.gds_client.get_exchange()
            inventory: Inventory = self.gds_client.get_inventory()
            price_data: PriceDataSnapshot = self.price_client.get_price_data_snapshot()

            logger.info("Refreshing buy limits")
            self.tdp_client.update_limits(cur_time)

            logger.info("Preparing strategies")
            strats_to_compute: List[BaseStrategy] = self.strat_manager.prepare_strats(cur_time)
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
                orders: List[Order] = self.order_executor.execute(
                    actions=actions,
                    calc_cycle=self.calc_cycle,
                    strat_name=strat.name,
                    cur_time=cur_time,
                )

                logger.info(f"Saving orders for strategy {strat.name}")
                self.tdp_client.save_orders(session_id=self.trade_session.session_id, orders=orders)

            duration: float = self.strat_manager.next_strat_wait_time(cur_time)
            self.wait(duration)

        logger.info("Exiting autotrader loop")

    def stop(self, signum: int, frame: Optional[types.FrameType]) -> None:
        logger.info(f"Received signal {signum}. Stopping auto trader")
        self.autotrader_active = False
        # TODO: save state of world, shutdown gracefully
