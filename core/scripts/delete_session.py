from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests
from redis import Redis
from requests import Response


GDS_HOST: str = "localhost"
GDS_PORT: int = 19100
REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0


@dataclass(frozen=True)
class ProgramArgs:
    session_id: Optional[str]


def get_program_args() -> ProgramArgs:
    parser: ArgumentParser = ArgumentParser(description="Script that deletes redis keys")
    parser.add_argument("--session-id", type=Optional[str], required=False, default=None, help="Session ID")

    args: Namespace = parser.parse_args()
    return ProgramArgs(**vars(args))


def get_session_id() -> str:
    resp: Response = requests.get(f"http://{GDS_HOST}:{GDS_PORT}/session")
    data: Dict[str, Any] = resp.json()
    return data["id"]


def main() -> None:
    args: ProgramArgs = get_program_args()

    session_id: str = args.session_id or get_session_id()

    redis_client: Redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    keys: List[str] = redis_client.keys(f"*.{session_id}")

    if not keys:
        print(f"No matching keys with session id {session_id}")
        return

    redis_client.delete(*keys)
    print(f"Deleted the following keys: {keys}")


if __name__ == "__main__":
    main()
