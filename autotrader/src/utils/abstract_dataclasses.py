from abc import ABC
from dataclasses import dataclass


@dataclass
class AbstractDataclass(ABC):
    def __new__(cls, *args, **kwargs):
        if cls == AbstractDataclass or AbstractDataclass in cls.__bases__:
            raise TypeError(f"Cannot instantiate abstract class {cls.__name__}")
        return super().__new__(cls)
