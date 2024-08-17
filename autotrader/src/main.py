from clients.gds_client import GdsClient
from clients.price_client import PriceClient
from config.app_config import AppConfig
from interface.controller import Controller
from interface.screen_locator import ScreenLocator
from trader import Trader


def create_trader() -> Trader:
    app_config: AppConfig = AppConfig()
    locator: ScreenLocator = ScreenLocator(randomize=app_config.humanize)
    controller: Controller = Controller(locator=locator, randomize=app_config.humanize)
    price_client: PriceClient = PriceClient(url=app_config.price_url)
    gds_client: GdsClient = GdsClient(gds_host=app_config.gds_host, gds_port=app_config.gds_port)
    return Trader(
        controller=controller,
        price_client=price_client,
        gds_client=gds_client,
    )


if __name__ == "__main__":
    trader: Trader = create_trader()
    trader.start()
