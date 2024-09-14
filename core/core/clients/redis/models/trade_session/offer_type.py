from enum import Enum


class OfferType(Enum):

    NOT_SPECIFIED = "NOT_SPECIFIED"
    CANCEL = "CANCEL"
    BUY = "BUY"
    SELL = "SELL"

    @classmethod
    def from_str(cls, order_type: str) -> "OfferType":
        try:
            return cls[order_type.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED
