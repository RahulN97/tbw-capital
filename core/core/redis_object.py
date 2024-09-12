import pickle
from dataclasses import dataclass

from core.abstract_dataclasses import AbstractDataclass


@dataclass
class RedisObject(AbstractDataclass):

    @classmethod
    def deserialize(cls, data: bytes) -> "RedisObject":
        return pickle.loads(data)

    def serialize(self) -> bytes:
        return pickle.dumps(self)
