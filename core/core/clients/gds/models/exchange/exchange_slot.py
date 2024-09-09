from dataclasses import dataclass

from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState


@dataclass
class ExchangeSlot:
    position: int
    item_id: int
    price: int
    quantity_transacted: int
    total_quantity: int
    state: ExchangeSlotState

    def is_same(self, slot: "ExchangeSlot") -> bool:
        return (
            self.position == slot.position
            and self.item_id == slot.item_id
            and self.price == slot.price
            and self.total_quantity == slot.total_quantity
        )
