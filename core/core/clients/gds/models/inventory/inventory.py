from dataclasses import dataclass
from typing import List

from core.clients.gds.models.inventory.item import Item
from core.redis_object import RedisObject


@dataclass
class Inventory(RedisObject):
    items: List[Item]
