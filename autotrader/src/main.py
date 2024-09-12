import time

from core.clients.gds.gds_client import GdsClient
from core.clients.price.price_client import PriceClient
from core.clients.redis.redis_client import RedisClient
from core.clients.tdp.tdp_client import TdpClient
from core.logger import logger

from config.autotrader_config import AutotraderConfig
from executor import OrderExecutor
from interface.controller import Controller
from interface.screen_locator import ScreenLocator
from strategy.strategy_factory import StrategyFactory
from trader import Trader


def create_trader(config: AutotraderConfig) -> Trader:
    redis_client: RedisClient = RedisClient(host=config.redis_host, port=config.redis_port)
    price_client: PriceClient = PriceClient()
    gds_client: GdsClient = GdsClient(host=config.gds_host, port=config.gds_port)
    tdp_client: TdpClient = TdpClient(host=config.tdp_host, port=config.tdp_port)

    locator: ScreenLocator = ScreenLocator(randomize=config.humanize)
    controller: Controller = Controller(locator=locator, randomize=config.humanize)
    order_executor: OrderExecutor = OrderExecutor(controller=controller, gds_client=gds_client)
    strat_factory: StrategyFactory = StrategyFactory(
        redis_client=redis_client,
        item_map=price_client.item_map,
        is_f2p=gds_client.is_f2p,
    )

    return Trader(
        env=config.env,
        autotrader_wait=config.autotrader_wait,
        controller=controller,
        order_executor=order_executor,
        price_client=price_client,
        gds_client=gds_client,
        tdp_client=tdp_client,
        strat_factory=strat_factory,
    )


def main() -> None:
    config: AutotraderConfig = AutotraderConfig()
    trader: Trader = create_trader(config)

    logger.info(f"Waiting {int(config.autotrader_start_delay)} seconds before autotrader is activated.")
    time.sleep(config.autotrader_start_delay)
    trader.start()


if __name__ == "__main__":
    main()
