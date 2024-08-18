from dataclasses import dataclass
from typing import List

from clients.gds.models.exchange.exchange_slot import ExchangeSlot


@dataclass
class Exchange:
    slots: List[ExchangeSlot]
