from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    x: int
    y: int
    x_jitter: int = 0
    y_jitter: int = 0
