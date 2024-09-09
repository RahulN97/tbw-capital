from dataclasses import dataclass
from typing import List

from core.clients.gds.models.exchange.exchange_slot import ExchangeSlot


@dataclass
class Exchange:
    slots: List[ExchangeSlot]
