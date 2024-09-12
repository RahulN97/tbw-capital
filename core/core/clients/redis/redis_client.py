from typing import Dict, List, Optional

from redis import Redis

from core.clients.base_client import BaseClient
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.redis.exceptions import RedisKeyError
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession


class RedisClient(BaseClient):

    REDIS_DB_MAP: Dict[str, int] = {
        "trade_session": 0,
        "buy_limit": 1,
    }

    def __init__(self, host: str, port: int) -> None:
        self.trades_client: Redis = Redis(host=host, port=port, db=self.REDIS_DB_MAP["trade_session"])
        self.limits_client: Redis = Redis(host=host, port=port, db=self.REDIS_DB_MAP["buy_limit"])
        super().__init__()

    def establish_connection(self) -> None:
        self.trades_client.ping()
        self.limits_client.ping()

    def get_buy_limit(self, item_id: int) -> BuyLimit:
        key: str = str(item_id)
        raw: Optional[bytes] = self.limits_client.hget(name="buy_limit", key=key)
        if raw is None:
            raise RedisKeyError(key=key)
        return BuyLimit.deserialize(raw)

    def set_buy_limit(self, buy_limit: BuyLimit) -> None:
        self.limits_client.hset(name="buy_limit", key=buy_limit.item_id, value=buy_limit.serialize())

    def get_all_buy_limits(self) -> Dict[int, BuyLimit]:
        buy_limits: Optional[Dict[str, bytes]] = self.limits_client.hgetall(name="buy_limit")
        if buy_limits is None:
            return {}
        return {int(item_id): BuyLimit.deserialize(raw) for item_id, raw in buy_limits.items()}

    def set_all_buy_limits(self, buy_limits: Dict[int, BuyLimit]) -> None:
        buy_limits_serialized: Dict[int, bytes] = {id: limit.serialize() for id, limit in buy_limits.items()}
        self.limits_client.hset(name="buy_limit", mapping=buy_limits_serialized)

    def get_exchange_snapshot(self) -> Exchange:
        raw: Optional[bytes] = self.limits_client.get(name="exchange")
        if raw is None:
            raise RedisKeyError(key="exchange")
        return Exchange.deserialize(raw)

    def set_exchange_snapshot(self, exchange: Exchange) -> None:
        self.limits_client.set(name="exchange", value=exchange.serialize())

    def get_trade_session(self, session_id: str) -> TradeSession:
        raw: Optional[bytes] = self.trades_client.get(name=session_id)
        if raw is None:
            raise RedisKeyError(key=session_id)
        return TradeSession.deserialize(raw)

    def set_trade_session(self, trade_session: TradeSession) -> None:
        self.trades_client.set(name=trade_session.session_id, value=trade_session.serialize())

    def get_trades(self, session_id: str) -> Dict[str, List[Trade]]:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        return trade_session.trades

    def append_trades(self, session_id: str, strat_name: str, trades: List[Trade]) -> None:
        trade_session: TradeSession = self.get_trade_session(session_id=session_id)
        if strat_name not in trade_session.trades:
            trade_session.trades[strat_name] = []
        trade_session.trades[strat_name].extend(trades)
        self.set_trade_session(trade_session=trade_session)
