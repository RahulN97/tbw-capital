class RedisKeyError(Exception):
    def __init__(self, key: str) -> None:
        super().__init__(f"Key {key} not found in Redis")
