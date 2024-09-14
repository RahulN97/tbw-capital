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
