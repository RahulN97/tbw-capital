from typing import Annotated

from core.clients.gds.gds_client import GdsClient
from core.clients.redis.redis_client import RedisClient
from fastapi import Depends

from config.tdp_config import TdpConfig
from tracking.book_keeper import BookKeeper


tdp_config: TdpConfig = TdpConfig()


def get_config() -> TdpConfig:
    return tdp_config


TdpConfigDep = Annotated[TdpConfig, Depends(get_config)]


def get_redis_client(config: TdpConfigDep) -> RedisClient:
    return RedisClient(host=config.redis_host, port=config.redis_port)


RedisClientDep = Annotated[RedisClient, Depends(get_redis_client)]


def get_gds_client(config: TdpConfigDep) -> GdsClient:
    return GdsClient(host=config.gds_host, port=config.gds_port)


GdsClientDep = Annotated[GdsClient, Depends(get_gds_client)]


def get_book_keeper(redis_client: RedisClientDep, gds_client: GdsClientDep) -> BookKeeper:
    return BookKeeper(redis_client=redis_client, gds_client=gds_client)


BookKeeperDep = Annotated[BookKeeper, Depends(get_book_keeper)]
