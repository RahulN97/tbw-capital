from enum import Enum


class Environment(Enum):

    NOT_SPECIFIED = "NOT_SPECIFIED"
    DEV = "DEV"
    PROD = "PROD"

    @classmethod
    def from_str(cls, container: str) -> "Environment":
        try:
            return cls[container.upper()]
        except KeyError:
            return cls.NOT_SPECIFIED
