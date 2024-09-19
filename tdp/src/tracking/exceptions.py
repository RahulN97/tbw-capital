from typing import Optional

from core.clients.gds.models.exchange.exchange_slot import ExchangeSlot
from core.clients.redis.models.trade_session.order import Order


class UnexpectedOrder(Exception):
    def __init__(self, slot: ExchangeSlot, order: Optional[Order]) -> None:
        msg: str = (
            f"Current exchange has offer: {str(slot)}, but book keeper has no matching active order"
            if order is None
            else f"Current exchange has offer: {str(slot)}, but book keeper has order: {str(order)}"
        )
        super().__init__(msg)


class UnbookedOrder(Exception):
    def __init__(self, prev_order: Order, new_order: Order) -> None:
        msg: str = (
            f"Attempting to overwrite active order {str(prev_order)} with new order {str(new_order)}."
            "Orders must be booked and processed into trades."
        )
        super().__init__(msg)
