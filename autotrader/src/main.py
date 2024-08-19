import time

from clients.gds.gds_client import GdsClient
from clients.price.price_client import PriceClient
from config.app_config import AppConfig
from interface.controller import Controller
from interface.screen_locator import ScreenLocator
from strategy.strategy_factory import StrategyFactory
from trader import Trader
from utils.logging import logger


def create_trader(app_config: AppConfig) -> Trader:
    app_config: AppConfig = AppConfig()
    locator: ScreenLocator = ScreenLocator(randomize=app_config.humanize)
    controller: Controller = Controller(locator=locator, randomize=app_config.humanize)
    price_client: PriceClient = PriceClient()
    gds_client: GdsClient = GdsClient(gds_host=app_config.gds_host, gds_port=app_config.gds_port)
    strat_factory: StrategyFactory = StrategyFactory()
    return Trader(
        autotrader_wait=app_config.autotrader_wait,
        controller=controller,
        price_client=price_client,
        gds_client=gds_client,
        strat_factory=strat_factory,
    )


def main() -> None:
    app_config: AppConfig = AppConfig()

    logger.info(f"Waiting {int(app_config.autotrader_start_delay)} seconds before autotrader is activated.")
    time.sleep(app_config.autotrader_start_delay)

    trader: Trader = create_trader(app_config)
    trader.start()


if __name__ == "__main__":
    main()
