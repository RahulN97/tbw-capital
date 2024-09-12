from core.clients.gds.gds_client import GdsClient
from core.clients.price.price_client import PriceClient
from core.clients.redis.redis_client import RedisClient


class PnlCalculator:

    def __init__(self, redis_client: RedisClient, gds_client: GdsClient, price_client: PriceClient) -> None:
        self.redis_client: RedisClient = redis_client
        self.gds_client: GdsClient = gds_client
        self.price_client: PriceClient = price_client


"""
TODO:
    - intro concept of Order in TradeSession. TradeSession has Orders and Trades - { srat_name: Order/Trade }
    - book keeper always saves down orders
    - book keeper maintains state about orders in GE
    - book keeper maintains state about items in inv
    - as these orders fully buy, sell, abort (fully or partially) - book keeper saves down trades

redis stores pnl snapshots

Given map { strat: List[Trade] }, calculate pnl
get current inv and exchange

for each strat,
    create map { item_id: List[Trade] }



"""
