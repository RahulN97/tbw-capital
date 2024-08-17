from typing import List

from clients.gds_client import GdsClient
from clients.price_client import PriceClient
from interface.controller import Controller
from models.order import OrderAction
from strategy.mm import MMStrategy
from strategy.strategy import BaseStrategy
from utils.logging import logger


class Trader:

    def __init__(self, controller: Controller, price_client: PriceClient, gds_client: GdsClient) -> None:
        self.controller: Controller = controller
        self.price_client: PriceClient = price_client
        self.gds_client: GdsClient = gds_client

    def is_autotrade_on(self) -> bool:
        """
        TODO:
        check if autotrade is toggled in live config
        """
        return True

    def is_player_ready(self) -> bool:
        """
        TODO:
        check if gds player data is in expected state
        """
        return True

    def prepare_player(self) -> None:
        """
        TODO:
        click compass, walk to ge tile, zoom to scale, press down
        if not is_ready, throw Exception
        """
        pass

    def prepare_strats(self) -> List[BaseStrategy]:
        return [MMStrategy()]

    def trade(self, actions: List[str]) -> None:
        self.controller.open_exchange()
        # TODO: implement trading steps
        self.controller.exit_exchange()

    def start(self) -> None:
        logger.info("Starting auto trader")

        strats: List[BaseStrategy] = self.prepare_strats()
        while self.is_autotrade_on():
            if not self.is_player_ready():
                logger.info("Preparing player at exchange")
                self.prepare_player()

            logger.info("Preparing strategies")
            strats: List[BaseStrategy] = self.prepare_strats()
            for strat in strats:
                actions: List[OrderAction] = strat.compute()
                self.trade(actions)
