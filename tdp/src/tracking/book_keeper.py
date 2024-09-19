from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot import ExchangeSlot
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.redis.exceptions import RedisKeyError
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.models.trade_session.offer_type import OfferType
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.redis.redis_client import RedisClient

from tracking.exceptions import UnbookedOrder, UnexpectedOrder
from tracking.slot_diff import SlotDiff


class BookKeeper:

    RESET_TIME_SECS: int = 4 * 60 * 60

    def __init__(self, redis_client: RedisClient, gds_client: GdsClient) -> None:
        self.redis_client: RedisClient = redis_client
        self.gds_client: GdsClient = gds_client

    def _load_prev_exchange(self, player_name: str) -> Exchange:
        try:
            return self.redis_client.get_exchange_snapshot(player_name=player_name)
        except RedisKeyError:
            prev_exchange: Exchange = self.gds_client.get_exchange()
            self.redis_client.set_exchange_snapshot(player_name=player_name, exchange=prev_exchange)
            return prev_exchange

    def _calc_slot_diffs(self, prev_exchange: Exchange, cur_exchange: Exchange) -> Dict[int, List[SlotDiff]]:
        item_diff_map: Dict[int, List[SlotDiff]] = defaultdict(list)

        for prev, cur in zip(prev_exchange.slots, cur_exchange.slots):
            if cur.state not in (ExchangeSlotState.BOUGHT, ExchangeSlotState.BUYING):
                continue

            bought: int = (
                cur.quantity_transacted - prev.quantity_transacted
                if cur.is_same(prev) and cur.quantity_transacted >= prev.quantity_transacted
                else cur.quantity_transacted
            )
            item_diff_map[cur.item_id].append(SlotDiff(item_id=cur.item_id, bought=bought))

        return item_diff_map

    def update_limits(self, player_name: str, cur_time: Optional[float] = None) -> None:
        cur_time: float = cur_time or datetime.now().timestamp()

        prev_exchange: Exchange = self._load_prev_exchange(player_name)
        cur_exchange: Exchange = self.gds_client.get_exchange()
        item_diff_map: Dict[int, List[SlotDiff]] = self._calc_slot_diffs(
            prev_exchange=prev_exchange,
            cur_exchange=cur_exchange,
        )

        buy_limits: Dict[int, BuyLimit] = self.redis_client.get_all_buy_limits(player_name=player_name)
        for item_id, buy_limit in buy_limits.items():
            if item_id in item_diff_map:
                for diff in item_diff_map[item_id]:
                    buy_limit.bought += diff.bought
                    if buy_limit.reset_time is None or buy_limit.reset_time < cur_time:
                        buy_limit.reset_time = cur_time + self.RESET_TIME_SECS
            else:
                if buy_limit.reset_time is not None and buy_limit.reset_time < cur_time:
                    buy_limit.reset_time = None
                    buy_limit.bought = 0

        self.redis_client.set_all_buy_limits(player_name=player_name, buy_limits=buy_limits)
        self.redis_client.set_exchange_snapshot(player_name=player_name, exchange=cur_exchange)

    def save_trade_session(self, session: TradeSession) -> None:
        self.redis_client.set_trade_session(session)

    def save_orders(self, session_id: str, orders: Dict[str, List[Order]]) -> None:
        active_orders: Dict[int, Order] = self.redis_client.get_active_orders(session_id=session_id)
        flattened_orders: List[Order] = [o for o_list in orders.values() for o in o_list]
        for order in flattened_orders:
            if order.metadata.ge_slot in active_orders:
                raise UnbookedOrder(prev_order=active_orders[order.metadata.ge_slot], new_order=order)
            active_orders[order.metadata.ge_slot] = order
        self.redis_client.append_orders(session_id=session_id, orders=orders)
        self.redis_client.set_active_orders(session_id=session_id, active_orders=active_orders)

    @staticmethod
    def _is_matching_offer(slot: ExchangeSlot, order: Order) -> bool:
        offer_type: OfferType = order.metadata.type
        matching_offer_type: bool = (
            (offer_type == OfferType.CANCEL_BUY and slot.state == ExchangeSlotState.CANCELLED_BUY)
            or (offer_type == OfferType.CANCEL_SELL and slot.state == ExchangeSlotState.CANCELLED_SELL)
            or (offer_type == OfferType.BUY and slot.state == ExchangeSlotState.BOUGHT)
            or (offer_type == OfferType.SELL and slot.state == ExchangeSlotState.SOLD)
        )
        return (
            matching_offer_type
            and slot.position == order.ge_slot
            and slot.item_id == order.metadata.item_id
            and slot.price == order.metadata.price
            and slot.total_quantity == order.metadata.quantity
        )

    def book_trades(self, session_id: str, calc_cycle: int, cur_time: Optional[float] = None) -> List[Trade]:
        cur_time: float = cur_time if cur_time is not None else datetime.now().timestamp()
        trades: Dict[str, List[Trade]] = defaultdict(list)

        active_orders: Dict[int, Order] = self.redis_client.get_active_orders(session_id=session_id)
        exchange: Exchange = self.gds_client.get_exchange()
        for slot in exchange.slots:
            if slot.state in (ExchangeSlotState.EMPTY, ExchangeSlotState.BUYING, ExchangeSlotState.SELLING):
                continue

            order: Optional[Order] = active_orders.get(slot.position)
            if order is None or not self._is_matching_offer(slot=slot, order=order):
                raise UnexpectedOrder(slot=slot, order=order)

            trades[order.strat_name].append(
                Trade(
                    id=order.id,
                    calc_cycle=calc_cycle,
                    strat_name=order.strat_name,
                    transacted=slot.quantity_transacted,
                    metadata=order.metadata,
                    time=cur_time,
                )
            )

            del active_orders[slot.position]

        self.redis_client.append_trades(session_id=session_id, trades=trades)
        self.redis_client.set_active_orders(session_id=session_id, active_orders=active_orders)
        return trades
