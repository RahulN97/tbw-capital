from typing import Dict, List, Optional

from redis import Redis

from core.clients.base_client import BaseClient
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.redis.exceptions import RedisKeyError
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.models.pnl.pnl import Pnl
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession


class RedisClient(BaseClient):

    REDIS_DB_MAP: Dict[str, int] = {
        "session": 0,
        "player": 1,
    }

    def __init__(self, host: str, port: int) -> None:
        self.session_client: Redis = Redis(host=host, port=port, db=self.REDIS_DB_MAP["session"])
        self.player_client: Redis = Redis(host=host, port=port, db=self.REDIS_DB_MAP["player"])
        super().__init__()

    def establish_connection(self) -> None:
        self.session_client.ping()
        self.player_client.ping()

    @staticmethod
    def _get_raw(client: Redis, name: str) -> bytes:
        raw: Optional[bytes] = client.get(name=name)
        if raw is None:
            raise RedisKeyError(key=name)
        return raw

    @staticmethod
    def _hget_raw(client: Redis, name: str, key: str) -> bytes:
        raw: Optional[bytes] = client.hget(name=name, key=key)
        if raw is None:
            raise RedisKeyError(key=key)
        return raw

    @staticmethod
    def _get_name(prefix: str, name: str) -> str:
        return f"{prefix}.{name.lower().replace(' ', '')}"

    def get_buy_limit(self, player_name: str, item_id: int) -> BuyLimit:
        name: str = self._get_name(prefix="buy_limit", name=player_name)
        raw: bytes = self._hget_raw(client=self.player_client, name=name, key=str(item_id))
        return BuyLimit.deserialize(raw)

    def set_buy_limit(self, player_name: str, buy_limit: BuyLimit) -> None:
        name: str = self._get_name(prefix="buy_limit", name=player_name)
        self.player_client.hset(name=name, key=buy_limit.item_id, value=buy_limit.serialize())

    def get_all_buy_limits(self, player_name: str) -> Dict[int, BuyLimit]:
        name: str = self._get_name(prefix="buy_limit", name=player_name)
        buy_limits: Optional[Dict[str, bytes]] = self.player_client.hgetall(name=name)
        if buy_limits is None:
            return {}
        return {int(item_id): BuyLimit.deserialize(raw) for item_id, raw in buy_limits.items()}

    def set_all_buy_limits(self, player_name: str, buy_limits: Dict[int, BuyLimit]) -> None:
        name: str = self._get_name(prefix="buy_limit", name=player_name)
        buy_limits_serialized: Dict[int, bytes] = {id: limit.serialize() for id, limit in buy_limits.items()}
        self.player_client.hset(name=name, mapping=buy_limits_serialized)

    def get_exchange_snapshot(self, player_name: str) -> Exchange:
        name: str = self._get_name(prefix="exchange", name=player_name)
        raw: bytes = self._get_raw(client=self.player_client, name=name)
        return Exchange.deserialize(raw)

    def set_exchange_snapshot(self, player_name: str, exchange: Exchange) -> None:
        name: str = self._get_name(prefix="exchange", name=player_name)
        self.player_client.set(name=name, value=exchange.serialize())

    def get_trade_session(self, session_id: str) -> TradeSession:
        name: str = self._get_name(prefix="trade_session", name=session_id)
        raw: bytes = self._get_raw(client=self.session_client, name=name)
        return TradeSession.deserialize(raw)

    def set_trade_session(self, trade_session: TradeSession) -> None:
        name: str = self._get_name(prefix="trade_session", name=trade_session.session_id)
        self.session_client.set(name=name, value=trade_session.serialize())

    def get_orders(self, session_id: str) -> Dict[str, List[Order]]:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        return trade_session.orders

    def append_orders(self, session_id: str, orders: Dict[str, List[Order]]) -> None:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        for strat_name, strat_orders in orders.items():
            if strat_name not in trade_session.orders:
                trade_session.orders[strat_name] = []
            trade_session.orders[strat_name].extend(strat_orders)
        self.set_trade_session(trade_session=trade_session)

    def get_trades(self, session_id: str) -> Dict[str, List[Trade]]:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        return trade_session.trades

    def append_trades(self, session_id: str, trades: Dict[str, List[Trade]]) -> None:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        for strat_name, strat_trades in trades.items():
            if strat_name not in trade_session.trades:
                trade_session.trades[strat_name] = []
            trade_session.trades[strat_name].extend(strat_trades)
        self.set_trade_session(trade_session=trade_session)

    def get_active_orders(self, session_id: str) -> Dict[int, Order]:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        return trade_session.active_orders

    def set_active_orders(self, session_id: str, active_orders: Dict[int, Order]) -> None:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        trade_session.active_orders = active_orders
        self.set_trade_session(trade_session=trade_session)

    def get_session_validity(self, session_id: str) -> bool:
        name: str = self._get_name(prefix="valid", name=session_id)
        raw: bytes = self._get_raw(client=self.session_client, name=name)
        return bool(raw)

    def set_session_validity(self, session_id: str, valid: bool) -> None:
        name: str = self._get_name(prefix="valid", name=session_id)
        self.session_client.set(name=name, value=bytes(valid))

    def get_pnl_snapshot(self, session_id: str) -> Pnl:
        name: str = self._get_name(prefix="pnl", name=session_id)
        raw: bytes = self._get_raw(client=self.session_client, name=name)
        return Pnl.deserialize(raw)

    def set_pnl_snapshot(self, session_id: str, pnl: Pnl) -> None:
        name: str = self._get_name(prefix="pnl", name=session_id)
        self.session_client.set(name=name, value=pnl.serialize())
