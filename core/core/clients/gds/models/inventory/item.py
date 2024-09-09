from dataclasses import dataclass


@dataclass
class Item:
    id: int
    quantity: int
    inventory_position: int
