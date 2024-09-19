import time
from collections import defaultdict
from datetime import datetime
from typing import Any, Callable, Dict, List, Set

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.price.models.price import LatestPrice
from core.clients.price.price_client import PriceClient
from core.clients.redis.models.pnl.pnl import Pnl
from core.clients.redis.models.pnl.pnl_snapshot import PnlCalcData, PnlSnapshot
from core.clients.redis.models.trade_session.offer_type import OfferType
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.redis.redis_client import RedisClient
from core.logger import logger

from constants import GP_ITEM_ID
from metrics.exceptions import UnexpectedExchangeSlotState, UnexpectedOfferType


class MetricsCalculator:

    def __init__(self, redis_client: RedisClient, gds_client: GdsClient, price_client: PriceClient) -> None:
        self.redis_client: RedisClient = redis_client
        self.gds_client: GdsClient = gds_client
        self.price_client: PriceClient = price_client

    @staticmethod
    def wait_for_lock(max_attempts: int, retry_wait: int) -> Callable:
        def wait_wrapper(f: Callable) -> Callable:
            def wait(self: "MetricsCalculator", *args, **kwargs) -> Any:
                attempt: int = 1
                while attempt <= max_attempts and not self.redis_client.get_session_validity(kwargs["session_id"]):
                    logger.info(f"Attempt {attempt} of reading resource failed. It's probably locked by autotrader")
                    time.sleep(retry_wait)
                    attempt += 1

                return f(self, *args, **kwargs)

            return wait

        return wait_wrapper

    def _assert_item_quantities_valid(
        self,
        trades_map: Dict[str, List[Trade]],
        start_items: Dict[int, int],
        inv: Inventory,
        exchange: Exchange,
    ) -> None:
        inv_items: Dict[int, int] = defaultdict(int)
        for item in inv.items:
            inv_items[item.id] += item.quantity

        sell_exch_items: Dict[int, int] = defaultdict(int)
        for slot in exchange.slots:
            if slot.state in (ExchangeSlotState.CANCELLED_SELL, ExchangeSlotState.SELLING, ExchangeSlotState.SOLD):
                sell_exch_items[slot.item_id] += slot.total_quantity

        item_to_trades: Dict[int, List[Trade]] = defaultdict(list)
        for trades in trades_map.values():
            for t in trades:
                item_to_trades[t.metadata.item_id].append(t)

        for item_id, trades in item_to_trades.items():
            start_qty: int = start_items.get(item_id, 0)
            trades_qty: int = sum(
                t.transacted if t.metadata.type in (OfferType.BUY, OfferType.CANCEL_BUY) else -1 * t.transacted
            )
            inv_qty: int = inv_items.get(item_id, 0)
            sell_qty: int = sell_exch_items.get(item_id, 0)
            assert start_qty + trades_qty == inv_qty + sell_qty

    def _calc_pnl(
        self,
        trades_map: Dict[str, List[Trade]],
        active_orders: Dict[int, Order],
        start_items: Dict[int, int],
    ) -> PnlSnapshot:
        inv: Inventory = self.gds_client.get_inventory()
        exchange: Exchange = self.gds_client.get_exchange()

        self._assert_item_quantities_valid(trades_map=trades_map, start_items=start_items, inv=inv, exchange=exchange)

        latest_prices: Dict[int, LatestPrice] = self.price_client.get_latest_prices()

        strat_pnl: Dict[str, int] = {}
        trade_ids: Dict[str, Set[str]] = defaultdict(set)
        strats: Set[str] = set(list(trades_map.keys()) + [o.strat_name for o in active_orders.values()])
        for strat in strats:
            item_trade_map: Dict[int, List[Trade]] = defaultdict(list)
            for trade in trades_map.get(strat, []):
                item_trade_map[trade.metadata.item_id].append(trade)

            pnl: int = 0
            for item_id, trades in item_trade_map.items():
                item_pnl: int = 0
                total_qty: int = 0
                for t in trades:
                    gp: int = t.metadata.quantity * t.metadata.price
                    if t.metadata.type in (OfferType.CANCEL_BUY, OfferType.BUY):
                        item_pnl -= gp
                        total_qty += t.metadata.quantity
                    elif t.metadata.type in (OfferType.CANCEL_SELL, OfferType.SELL):
                        item_pnl += gp
                        total_qty -= t.metadata.quantity
                    else:
                        raise UnexpectedOfferType(type=t.metadata.type)
                    trade_ids[strat].add(t.id)

                if total_qty > 0:
                    item_pnl += total_qty * latest_prices[item_id].low_price

                pnl += item_pnl

            strat_pnl[strat] = pnl

        calc_data: PnlCalcData = PnlCalcData(
            trade_ids=trade_ids,
            inv_snapshot=inv,
            exchange_snapshot=exchange,
            prices_snapshot=latest_prices,
        )
        return PnlSnapshot(strat_pnl=strat_pnl, calc_data=calc_data, update_time=datetime.now().timestamp())

    @wait_for_lock(max_attempts=10, retry_wait=5)
    def get_pnl(self, session_id: str) -> Pnl:
        trade_session: TradeSession = self.redis_client.get_trade_session(session_id=session_id)

        pnl_snapshot: PnlSnapshot = self._calc_pnl(
            trades_map=trade_session.trades,
            active_orders=trade_session.active_orders,
            start_items=trade_session.start_metadata.start_items,
        )

        prev_pnl: Pnl = self.redis_client.get_pnl_snapshot(session_id=session_id)
        pnl_snapshots: List[PnlSnapshot] = prev_pnl.pnl_snapshots.append(pnl_snapshot)
        return Pnl(
            session_id=session_id,
            total_pnl=sum(pnl_snapshot.strat_pnl.values()),
            pnl_snapshots=pnl_snapshots,
            update_time=datetime.now().timestamp(),
        )

    @wait_for_lock(max_attempts=10, retry_wait=5)
    def get_nw(self, session_id: str) -> int:
        inv: Inventory = self.gds_client.get_inventory()
        exchange: Exchange = self.gds_client.get_exchange()
        prices: Dict[int, LatestPrice] = self.price_client.get_latest_prices()

        nw: int = 0
        for item in inv.items:
            if item.id == GP_ITEM_ID:
                nw += item.quantity
            elif item.id in prices:
                nw += item.quantity * prices[item.id].low_price

        for slot in exchange.slots:
            if slot.state == ExchangeSlotState.EMPTY:
                continue

            item_price: int = 1 if slot.item_id == GP_ITEM_ID else prices[slot.item_id].low_price
            if slot.state in (ExchangeSlotState.CANCELLED_BUY, ExchangeSlotState.BUYING, ExchangeSlotState.BOUGHT):
                item_value: int = slot.quantity_transacted * item_price
                cash_value: int = (slot.total_quantity - slot.quantity_transacted) * slot.price
            elif slot.state in (ExchangeSlotState.CANCELLED_SELL, ExchangeSlotState.SELLING, ExchangeSlotState.SOLD):
                item_value: int = (slot.total_quantity - slot.quantity_transacted) * item_price
                cash_value: int = slot.quantity_transacted * slot.price
            else:
                raise UnexpectedExchangeSlotState(state=slot.state)

            nw += item_value
            nw += cash_value

        return nw
