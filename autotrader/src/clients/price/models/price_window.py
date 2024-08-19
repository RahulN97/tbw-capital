from enum import Enum, auto


class PriceWindow(Enum):

    NOT_SPECIFIED = auto()
    AVG_5M = auto()
    AVG_1H = auto()
