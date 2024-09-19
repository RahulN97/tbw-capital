from argparse import ArgumentParser, Namespace
from dataclasses import dataclass
from typing import List

from redis import Redis


REDIS_HOST: str = "localhost"
REDIS_PORT: int = 6379
REDIS_DB: int = 0


@dataclass(frozen=True)
class ProgramArgs:
    session_id: str


def get_program_args() -> ProgramArgs:
    parser: ArgumentParser = ArgumentParser(description="Script that deletes redis keys")
    parser.add_argument("--session-id", type=str, required=True, help="Session ID")

    args: Namespace = parser.parse_args()
    return ProgramArgs(**vars(args))


def main() -> None:
    args: ProgramArgs = get_program_args()

    redis_client: Redis = Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)
    keys: List[str] = redis_client.keys(f"*.{args.session_id}")

    if not keys:
        print(f"No matching keys with session id {args.session_id}")
        return

    redis_client.delete(*keys)
    print(f"Deleted the following keys: {keys}")


if __name__ == "__main__":
    main()
