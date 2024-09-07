from dataclasses import dataclass


@dataclass
class BuyLimit:
    item_id: int
    bought: int
    limit: int
    reset_time: float
