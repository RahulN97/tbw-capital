from dataclasses import dataclass


@dataclass(frozen=True)
class SlotDiff:
    item_id: int
    bought: int
