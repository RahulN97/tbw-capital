from collections import defaultdict
from typing import Dict, List

from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.redis.redis_client import RedisClient
from core.tracking.slot_diff import SlotDiff


class BookKeeper:

    RESET_TIME_SECS: int = 4 * 60 * 60

    def __init__(self, redis_client: RedisClient, gds_client: GdsClient) -> None:
        self.redis_client: RedisClient = redis_client
        self.gds_client: GdsClient = gds_client
        self.prev_exchange: Exchange = gds_client.get_exchange()

    def calc_slot_diffs(self, cur_exchange: Exchange) -> Dict[int, List[SlotDiff]]:
        item_diff_map: Dict[int, List[SlotDiff]] = defaultdict(list)

        for prev, cur in zip(self.prev_exchange.slots, cur_exchange.slots):
            if cur.state not in (ExchangeSlotState.BOUGHT, ExchangeSlotState.BUYING):
                continue

            bought: int = (
                cur.quantity_transacted - prev.quantity_transacted
                if cur.is_same(prev) and cur.quantity_transacted >= prev.quantity_transacted
                else cur.quantity_transacted
            )
            item_diff_map[cur.item_id].append(SlotDiff(item_id=cur.item_id, bought=bought))

        return item_diff_map

    def update_limits(self, cur_time: float) -> None:
        cur_exchange: Exchange = self.gds_client.get_exchange()
        item_diff_map: Dict[int, List[SlotDiff]] = self.calc_slot_diffs(cur_exchange)

        buy_limits: Dict[int, BuyLimit] = self.redis_client.get_all_buy_limits()
        for item_id, buy_limit in buy_limits.items():
            if item_id in item_diff_map:
                for diff in item_diff_map[item_id]:
                    buy_limit.bought += diff.bought
                    if buy_limit.reset_time is None or buy_limit.reset_time < cur_time:
                        buy_limit.reset_time = cur_time + self.RESET_TIME_SECS
            else:
                if buy_limit.reset_time < cur_time:
                    buy_limit.reset_time = None
                    buy_limit.bought = 0

        self.redis_client.set_all_buy_limits(buy_limits)
        self.prev_exchange: Exchange = cur_exchange

    def save_trade_session(self, session: TradeSession) -> None:
        self.redis_client.set_trade_session(session)

    def save_trades(self, actions, strat_name: str) -> None:
        pass
