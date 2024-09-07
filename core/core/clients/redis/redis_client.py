from typing import Dict

from redis import Redis

from core.clients.base_client import BaseClient
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
        self.trade_db: Redis = Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB_MAP["trade_session"],
        )
        self.limit_db: Redis = Redis(
            host=self.REDIS_HOST,
            port=self.REDIS_PORT,
            db=self.REDIS_DB_MAP["buy_limit"],
        )
        super().__init__()

    def establish_connection(self) -> None:
        self.trade_db.ping()
        self.limit_db.ping()

    def get_buy_limit(self, item_id: int) -> BuyLimit:
        pass

    def set_buy_limit(self, buy_limit: BuyLimit) -> None:
        pass

    def get_trade_session(self, session_id: str) -> TradeSession:
        pass

    def set_trade_session(self, trade_session: TradeSession) -> None:
        pass
