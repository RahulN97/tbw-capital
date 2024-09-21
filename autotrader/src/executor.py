import random
import time
from datetime import datetime
from typing import Any, Callable, Dict, List
from uuid import uuid4

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.chat.chat_box import ChatBox
from core.clients.gds.models.chat.message import Message
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot import ExchangeSlot
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.redis.models.trade_session.offer_metadata import OfferMetadata
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.redis_client import RedisClient
from core.clients.tdp.tdp_client import TdpClient
from core.logger import logger

from exceptions import MissingInventoryItemError, NoAvailableGeSlotError, PlayerStateError, UnsupportedOrderActionError
from interface.controller import Controller
from strategy.action import BuyAction, CancelOrderAction, InputOrderAction, OrderAction, SellAction


class OrderExecutor:

    MIN_ORDER_ACTION_PAUSE: float = 0.5
    MAX_ORDER_ACTION_PAUSE: float = 1.5

    def __init__(
        self,
        controller: Controller,
        redis_client: RedisClient,
        gds_client: GdsClient,
        tdp_client: TdpClient,
    ) -> None:
        self.controller: Controller = controller
        self.redis_client: RedisClient = redis_client
        self.gds_client: GdsClient = gds_client
        self.tdp_client: TdpClient = tdp_client

        self.session_id: str = gds_client.session_metadata.id
        self.player_name: str = gds_client.session_metadata.player_name
        self.session_start: float = gds_client.session_metadata.start_time
        self.abort: bool = False

    @staticmethod
    def check_abort(f: Callable) -> Callable:
        def check(self: "OrderExecutor", *args, **kwargs) -> Any:
            if self.abort:
                raise Exception("Autotrader process terminated unexpectedly. Interrupting order executor.")
            return f(self, *args, **kwargs)

        return check

    @staticmethod
    def control_ge_interface(f: Callable) -> Callable:
        def use_ge(self: "OrderExecutor", *args, **kwargs) -> Any:
            self.controller.open_ge()
            result: Any = f(self, *args, **kwargs)
            self.controller.exit_ge()
            return result

        return use_ge

    def _sent_public_chat(self) -> bool:
        chat: ChatBox = self.gds_client.get_chat_box()
        messages: List[Message] = [m for m in chat.messages if m.time >= self.session_start]
        return any(msg.sender == self.player_name for msg in messages)

    def _get_next_available_ge_slot(self) -> int:
        exchange: Exchange = self.gds_client.get_exchange()
        for slot in exchange.slots:
            if slot.state == ExchangeSlotState.EMPTY:
                return slot.position
        raise NoAvailableGeSlotError()

    def _get_inv_slot(self, item_id: int) -> int:
        inventory: Inventory = self.gds_client.get_inventory()
        for item in inventory.items:
            if item.id == item_id:
                return item.inventory_position
        raise MissingInventoryItemError(item_id)

    @check_abort
    def _cancel_order(self, ge_slot: int) -> None:
        logger.info(f"Attempting to cancel order in GE slot: {ge_slot}")
        self.controller.click_ge_slot(ge_slot)
        self.controller.click_location("ge_abort_offer")
        self.controller.click_location("ge_back")

    @check_abort
    def _input_order(self, order: InputOrderAction) -> None:
        self.controller.click_location("ge_enter_quantity")
        self.controller.type(str(order.quantity))
        self.controller.press("enter")

        self.controller.click_location("ge_enter_price")
        self.controller.type(str(order.price))
        self.controller.press("enter")

        self.controller.click_location("ge_confirm")

    @check_abort
    def _handle_order(self, action: OrderAction) -> int:
        if isinstance(action, CancelOrderAction):
            self._cancel_order(action.ge_slot)
            return action.ge_slot

        if isinstance(action, InputOrderAction):
            ge_slot: int = self._get_next_available_ge_slot()
            if isinstance(action, BuyAction):
                self.controller.click_ge_slot(ge_slot)
                self.controller.type(action.item_name)
                self.controller.press("enter")
            elif isinstance(action, SellAction):
                inv_slot: int = self._get_inv_slot(action.item_id)
                self.controller.click_inventory_slot(inv_slot)
            else:
                raise UnsupportedOrderActionError(
                    actual=type(action).__name__,
                    expected=InputOrderAction.__name__,
                )
            order_msg: str = f"item {action.item_name}, price: {action.price}, quantity: {action.quantity}"
            logger.info(f"Submitting {type(action).__name__} in GE slot {ge_slot} - {order_msg}")
            self._input_order(action)
            return ge_slot

        raise UnsupportedOrderActionError(
            actual=type(action).__name__,
            expected=OrderAction.__name__,
        )

    def _create_order(
        self,
        action: OrderAction,
        calc_cycle: int,
        strat_name: str,
        ge_slot: int,
        cur_time: float,
    ) -> Order:
        if isinstance(action, CancelOrderAction):
            exchange: Exchange = self.gds_client.get_exchange()
            slot: ExchangeSlot = next(s for s in exchange.slots if s.position == ge_slot)
            item_id: int = slot.item_id
            price: int = slot.price
            quantity: int = slot.total_quantity
        elif isinstance(action, InputOrderAction):
            item_id: int = action.item_id
            price: int = action.price
            quantity: int = action.quantity
        else:
            raise UnsupportedOrderActionError(
                actual=type(action).__name__,
                expected=OrderAction.__name__,
            )

        metadata: OfferMetadata = OfferMetadata(
            type=action.get_offer_type(),
            item_id=item_id,
            price=price,
            quantity=quantity,
            ge_slot=ge_slot,
        )
        return Order(
            id=str(uuid4()),
            calc_cycle=calc_cycle,
            strat_name=strat_name,
            metadata=metadata,
            time=cur_time,
        )

    @control_ge_interface
    def execute(self, actions: List[OrderAction], calc_cycle: int, strat_name: str) -> None:
        orders: List[Order] = []

        for action in actions:
            action_pause: float = random.uniform(self.MIN_ORDER_ACTION_PAUSE, self.MAX_ORDER_ACTION_PAUSE)
            time.sleep(action_pause)

            if self._sent_public_chat():
                raise PlayerStateError("Player sent a message in chat box. Aborting to avoid bot detection")

            ge_slot: int = self._handle_order(action)
            orders.append(
                self._create_order(
                    action=action,
                    calc_cycle=calc_cycle,
                    strat_name=strat_name,
                    ge_slot=ge_slot,
                    cur_time=datetime.now().timestamp(),
                )
            )

        logger.info(f"Saving {len(orders)} orders generated by strat")
        self.tdp_client.save_orders(session_id=self.session_id, orders=orders)

    @control_ge_interface
    def book_trades(self, calc_cycle: int, cur_time: float) -> None:
        trades_map: Dict[str, List[Trade]] = self.tdp_client.book_trades(
            session_id=self.session_id,
            calc_cycle=calc_cycle,
            time=cur_time,
        )
        trades: List[Trade] = [t for trade_list in trades_map.values() for t in trade_list]

        exchange: Exchange = self.gds_client.get_exchange()
        slots: List[ExchangeSlot] = [
            s
            for s in exchange.slots
            if s.state not in (ExchangeSlotState.BUYING, ExchangeSlotState.SELLING, ExchangeSlotState.EMPTY)
        ]

        assert len(trades) == len(slots), f"TDP booked {len(trades)} trades, but {len(slots)} slots are ready"
        assert set(t.metadata.ge_slot for t in trades) == set(s.position for s in slots)

        for slot in slots:
            self.controller.click_ge_slot(slot.position)
            self.controller.click_location("ge_collect_coins")
            self.controller.click_location("ge_collect_items")

    @control_ge_interface
    def liquidate(self) -> None:
        exchange: Exchange = self.gds_client.get_exchange()
        for slot in exchange.slots:
            if slot.state in (ExchangeSlotState.BUYING, ExchangeSlotState.SELLING):
                self._cancel_order(slot.position)

        self.controller.click_location("ge_collect")
