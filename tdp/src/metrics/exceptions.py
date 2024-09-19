from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.redis.models.trade_session.offer_type import OfferType


class UnexpectedOfferType(Exception):
    def __init__(self, type: OfferType) -> None:
        super().__init__(f"Unexpected offer type: {type.name}")


class UnexpectedExchangeSlotState(Exception):
    def __init__(self, state: ExchangeSlotState) -> None:
        super().__init__(f"Unexpected exchange slot state: {state.name}")
