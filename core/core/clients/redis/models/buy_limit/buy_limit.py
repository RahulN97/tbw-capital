from dataclasses import dataclass
from typing import Optional

from core.redis_object import RedisObject


@dataclass
class BuyLimit(RedisObject):
    item_id: int
    bought: int
    limit: int
    reset_time: Optional[float] = None
