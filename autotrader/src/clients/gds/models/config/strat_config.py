from dataclasses import dataclass, field

from utils.abstract_dataclasses import AbstractDataclass


@dataclass
class StratConfig(AbstractDataclass):
    activated: bool
    wait_duration: int  # seconds
    max_offer_time: int  # seconds
    strat_name: str  # default arg in child classes


@dataclass
class MMStratConfig(StratConfig):
    strat_name: str = field(default="mmstrategy")
