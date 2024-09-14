from enum import Enum, auto


class ExchangeSlotState(Enum):

    NOT_SPECIFIED = auto()
    EMPTY = auto()
    CANCELLED_BUY = auto()
    BUYING = auto()
    BOUGHT = auto()
    CANCELLED_SELL = auto()
    SELLING = auto()
    SOLD = auto()

    @classmethod
    def from_str(cls, state: str) -> "ExchangeSlotState":
        try:
            return cls[state.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED
