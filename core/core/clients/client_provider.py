from core.clients.price.price_client import PriceClient
from core.clients.redis.redis_client import RedisClient
from core.clients.tdp.tdp_client import TdpClient
from core.generated.gds import ApiClient, Configuration
from core.generated.gds.api.gds_api import GdsApi
from core.generated.gds.models.health import Health


def provide_gds_client(host: str, port: int) -> GdsApi:
    config: Configuration = Configuration(host=f"http://{host}:{port}")
    api: GdsApi = GdsApi(api_client=ApiClient(config))

    health: Health = api.health_get()
    if health.status != "healthy":
        raise ConnectionError(f"RuneLite server health status: {health.status}")

    return api


def provide_price_client() -> PriceClient:
    client: PriceClient = PriceClient()

    if not client.item_map:
        raise ConnectionError("OSRS prices API is not returning any item metadata")
    if not client.get_latest_prices():
        raise ConnectionError("OSRS prices API is not returning any price data")

    return client


def provide_redis_client(host: str, port: int) -> RedisClient:
    client: RedisClient = RedisClient(host=host, port=port)

    client.session_client.ping()
    client.player_client.ping()

    return client


def provide_tdp_client(host: str, port: int) -> None:
    client: TdpClient = TdpClient(host=host, port=port)

    # TODO: establish connection

    return client
