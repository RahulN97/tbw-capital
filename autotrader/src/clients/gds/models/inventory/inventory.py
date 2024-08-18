from dataclasses import dataclass
from typing import List

from clients.gds.models.inventory.item import Item


@dataclass
class Inventory:
    items: List[Item]
