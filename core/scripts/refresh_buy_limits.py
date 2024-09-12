from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Set

import requests

from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.redis_client import RedisClient


MAX_INT: int = 2**31 - 1


@dataclass(frozen=True)
class ProgramArgs:
    redis_host: str
    redis_port: int
    item_ids: Optional[Set[int]] = None


def get_program_args() -> ProgramArgs:
    parser: ArgumentParser = ArgumentParser(description="Script that loads buy limits into redis")
    parser.add_argument("--redis-host", type=str, required=True, help="Redis server host")
    parser.add_argument("--redis-port", type=int, required=True, help="Redis server port")
    parser.add_argument(
        "--item-ids",
        type=lambda v: set(int(x) for x in v.split(",")),
        required=False,
        default=None,
        help="List of item ids to refresh buy limit for",
    )

    args: Namespace = parser.parse_args()
    return ProgramArgs(**vars(args))


def create_buy_limits(item_ids: Optional[Set[int]]) -> Dict[int, BuyLimit]:
    resp: requests.Response = requests.get(
        url="https://prices.runescape.wiki/api/v1/osrs/mapping",
        headers={"User-Agent": "tbw-capital@gmail.com"},
    )
    data: List[Dict[str, Any]] = resp.json()
    if item_ids is not None:
        data: List[Dict[str, Any]] = [d for d in data if d["id"] in item_ids]

    return {d["id"]: BuyLimit(item_id=d["id"], bought=0, limit=d.get("limit", MAX_INT)) for d in data}


def main() -> None:
    args: ProgramArgs = get_program_args()

    buy_limits: Dict[int, BuyLimit] = create_buy_limits(args.item_ids)

    redis_client: RedisClient = RedisClient(host=args.redis_host, port=args.redis_port)
    redis_client.set_all_buy_limits(buy_limits)


if __name__ == "__main__":
    main()
