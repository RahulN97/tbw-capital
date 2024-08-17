from dataclasses import dataclass


@dataclass(frozen=True)
class Location:
    x: int
    y: int
    x_jitter: int
    y_jitter: int
