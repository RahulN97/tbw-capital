import time

from core.clients.redis.redis_client import RedisClient
from core.logger import logger

from clients.gds.gds_client import GdsClient
from clients.price.price_client import PriceClient
from config.autotrader_config import AutotraderConfig
from interface.controller import Controller
from interface.screen_locator import ScreenLocator
from strategy.strategy_factory import StrategyFactory
from trader import Trader


def create_trader(config: AutotraderConfig) -> Trader:
    config: AutotraderConfig = AutotraderConfig()

    locator: ScreenLocator = ScreenLocator(randomize=config.humanize)
    controller: Controller = Controller(locator=locator, randomize=config.humanize)

    redis_client: RedisClient = RedisClient()
    price_client: PriceClient = PriceClient()
    gds_client: GdsClient = GdsClient(gds_host=config.gds_host, gds_port=config.gds_port)

    strat_factory: StrategyFactory = StrategyFactory(
        redis_client=redis_client,
        price_client=price_client,
        is_f2p=gds_client.is_f2p,
    )

    return Trader(
        env=config.env,
        autotrader_wait=config.autotrader_wait,
        controller=controller,
        redis_client=redis_client,
        price_client=price_client,
        gds_client=gds_client,
        strat_factory=strat_factory,
    )


def main() -> None:
    config: AutotraderConfig = AutotraderConfig()

    logger.info(f"Waiting {int(config.autotrader_start_delay)} seconds before autotrader is activated.")
    time.sleep(config.autotrader_start_delay)

    trader: Trader = create_trader(config)
    trader.start()


if __name__ == "__main__":
    main()
