from enum import Enum


class ItemContainer(Enum):

    NOT_SPECIFIED = "NOT_SPECIFIED"
    ALL = "ALL"
    EXCHANGE = "EXCHANGE"
    INVENTORY = "INVENTORY"

    @classmethod
    def from_str(cls, container: str) -> "ItemContainer":
        try:
            return cls[container.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED
