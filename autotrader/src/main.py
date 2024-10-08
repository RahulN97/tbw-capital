import time

from core.clients.gds.gds_client import GdsClient
from core.clients.price.price_client import PriceClient
from core.clients.redis.redis_client import RedisClient
from core.clients.tdp.tdp_client import TdpClient
from core.logger import logger

from config.autotrader_config import AutotraderConfig
from executor import OrderExecutor
from interface.controller import Controller
from interface.player import Player
from interface.screen_locator import ScreenLocator
from strategy.strategy_factory import StrategyFactory
from strategy.strategy_manager import StrategyManager
from trader import Trader


def create_trader(config: AutotraderConfig) -> Trader:
    redis_client: RedisClient = RedisClient(host=config.redis_host, port=config.redis_port)
    price_client: PriceClient = PriceClient()
    gds_client: GdsClient = GdsClient(host=config.gds_host, port=config.gds_port)
    tdp_client: TdpClient = TdpClient(host=config.tdp_host, port=config.tdp_port)

    locator: ScreenLocator = ScreenLocator(randomize=config.humanize)
    controller: Controller = Controller(locator=locator, randomize=config.humanize)
    player: Player = Player(controller=controller, gds_client=gds_client)
    order_executor: OrderExecutor = OrderExecutor(
        controller=controller,
        redis_client=redis_client,
        gds_client=gds_client,
        tdp_client=tdp_client,
    )

    strat_factory: StrategyFactory = StrategyFactory(
        redis_client=redis_client,
        item_map=price_client.item_map,
        is_f2p=gds_client.session_metadata.is_f2p,
    )
    strat_manager: StrategyManager = StrategyManager(strat_factory=strat_factory, gds_client=gds_client)

    return Trader(
        env=config.env,
        autotrader_wait=config.autotrader_wait,
        redis_client=redis_client,
        price_client=price_client,
        gds_client=gds_client,
        tdp_client=tdp_client,
        player=player,
        order_executor=order_executor,
        strat_manager=strat_manager,
    )


def main() -> None:
    config: AutotraderConfig = AutotraderConfig()

    logger.info(f"Waiting {int(config.autotrader_start_delay)} seconds before autotrader is activated.")
    time.sleep(config.autotrader_start_delay)

    trader: Trader = create_trader(config)
    trader.start()


if __name__ == "__main__":
    main()
