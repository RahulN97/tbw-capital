from dataclasses import dataclass

from utils.abstract_dataclasses import AbstractDataclass


@dataclass
class StratConfig(AbstractDataclass):
    activated: bool
    wait_duration: int  # seconds
    max_offer_time: int  # seconds


@dataclass
class MMStratConfig(StratConfig):
    pass
