import json
from dataclasses import dataclass

from core.abstract_dataclasses import AbstractDataclass


@dataclass
class RedisObject(AbstractDataclass):

    @classmethod
    def deserialize(cls, s: str) -> "RedisObject":
        return cls(**json.loads(s))

    def serialize(self) -> str:
        return json.dumps(vars(self))
