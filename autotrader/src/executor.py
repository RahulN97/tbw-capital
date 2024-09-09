import random
import time
from typing import List

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.gds.models.inventory.inventory import Inventory
from core.logger import logger

from exceptions import MissingInventoryItemError, NoAvailableGeSlotError, UnsupportedOrderActionError
from interface.controller import Controller
from models.order import BuyOrder, CancelOrder, InputOrder, OrderAction, SellOrder


class OrderExecutor:

    MIN_ORDER_ACTION_PAUSE: float = 0.5
    MAX_ORDER_ACTION_PAUSE: float = 1.5

    def __init__(self, controller: Controller, gds_client: GdsClient) -> None:
        self.controller: Controller = controller
        self.gds_client: GdsClient = gds_client
        self.abort: bool = False

    def get_next_available_ge_slot(self) -> int:
        exchange: Exchange = self.gds_client.get_exchange()
        for slot in exchange.slots:
            if slot.state == ExchangeSlotState.EMPTY:
                return slot.position
        raise NoAvailableGeSlotError()

    def get_inv_slot(self, item_id: int) -> int:
        inventory: Inventory = self.gds_client.get_inventory()
        for item in inventory.items:
            if item.id == item_id:
                return item.inventory_position
        raise MissingInventoryItemError(item_id)

    def input_order(self, order: InputOrder) -> None:
        self.controller.click_location("ge_enter_quantity")
        self.controller.type(str(order.quantity))
        self.controller.press("enter")

        self.controller.click_location("ge_enter_price")
        self.controller.type(str(order.price))
        self.controller.press("enter")

        self.controller.click_location("ge_confirm")

    def handle_order(self, action: OrderAction) -> None:
        if isinstance(action, CancelOrder):
            logger.info(f"Cancelling order in GE slot: {action.ge_slot}")
            self.controller.click_ge_slot(action.ge_slot)
            self.controller.click_location("ge_abort_offer")
            self.controller.click_location("ge_back")
        elif isinstance(action, InputOrder):
            ge_slot: int = self.get_next_available_ge_slot()
            if isinstance(action, BuyOrder):
                self.controller.click_ge_slot(ge_slot)
                self.controller.type(action.item_name)
                self.controller.press("enter")
            elif isinstance(action, SellOrder):
                inv_slot: int = self.get_inv_slot(action.item_id)
                self.controller.click_inventory_slot(inv_slot)
            else:
                raise UnsupportedOrderActionError(
                    actual=type(action).__name__,
                    expected=InputOrder.__name__,
                )
            order_msg: str = f"item {action.item_name}, price: {action.price}, quantity: {action.quantity}"
            logger.info(f"Submitting {type(action).__name__} in GE slot {ge_slot} - {order_msg}")
            self.input_order(action)
        else:
            raise UnsupportedOrderActionError(
                actual=type(action).__name__,
                expected=OrderAction.__name__,
            )

    def execute(self, actions: List[OrderAction]) -> None:
        self.controller.open_ge()

        for action in actions:
            action_pause: float = random.uniform(self.MIN_ORDER_ACTION_PAUSE, self.MAX_ORDER_ACTION_PAUSE)
            time.sleep(action_pause)

            if self.abort:
                raise Exception("Autotrader process terminated unexpectedly")

            self.handle_order(action)

        self.controller.exit_ge()
