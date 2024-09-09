from typing import Dict, Optional

from redis import Redis

from core.clients.base_client import BaseClient
from core.clients.redis.exceptions import RedisKeyNotFoundError
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.models.trade_session.trade_session import TradeSession


class RedisClient(BaseClient):

    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB_MAP: Dict[str, int] = {
        "trade_session": 0,
        "buy_limit": 1,
    }

    def __init__(self) -> None:
        self.trades_client: Redis = Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB_MAP["trade_session"],
        )
        self.limits_client: Redis = Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB_MAP["buy_limit"],
        )
        super().__init__()

    def establish_connection(self) -> None:
        self.trades_client.ping()
        self.limits_client.ping()

    def get_buy_limit(self, item_id: int) -> BuyLimit:
        raw: Optional[str] = self.limits_client.hget(name="buy_limit", key=str(item_id))
        if raw is None:
            raise RedisKeyNotFoundError(key=str(item_id))
        return BuyLimit.deserialize(raw)

    def get_all_buy_limits(self) -> Dict[int, BuyLimit]:
        buy_limits: Optional[Dict[str, str]] = self.limits_client.hgetall(name="buy_limit")
        if buy_limits is None:
            return {}
        return {int(item_id): BuyLimit.deserialize(raw) for item_id, raw in buy_limits.items()}

    def set_buy_limit(self, buy_limit: BuyLimit) -> None:
        self.limits_client.hset(name="buy_limit", key=buy_limit.item_id, value=buy_limit.serialize())

    def set_all_buy_limits(self, buy_limits: Dict[int, BuyLimit]) -> None:
        self.limits_client.hset(name="buy_limit", mapping=buy_limits)

    def get_trade_session(self, session_id: str) -> TradeSession:
        raw: Optional[str] = self.trades_client.get(name=session_id)
        if raw is None:
            raise RedisKeyNotFoundError(key=session_id)
        return TradeSession.deserialize(raw)

    def set_trade_session(self, trade_session: TradeSession) -> None:
        self.trades_client.set(name=trade_session.session_id, value=trade_session.serialize())
