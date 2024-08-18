from dataclasses import dataclass

from clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState


@dataclass
class ExchangeSlot:
    position: int
    item_id: int
    price: int
    quantity_transacted: int
    total_quantity: int
    state: ExchangeSlotState
