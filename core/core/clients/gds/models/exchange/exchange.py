from dataclasses import dataclass
from typing import List

from core.clients.gds.models.exchange.exchange_slot import ExchangeSlot
from core.redis_object import RedisObject


@dataclass
class Exchange(RedisObject):
    slots: List[ExchangeSlot]
