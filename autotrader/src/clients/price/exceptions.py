from typing import FrozenSet

from clients.price.models.price_window import PriceWindow


class PriceApiError(Exception):
    def __init__(self, error_msg: str) -> None:
        msg: str = f"Prices API call failed with error: {error_msg}."
        super().__init__(msg)


class UnsupportedPriceWindowError(Exception):
    def __init__(self, actual: PriceWindow, supported: FrozenSet[PriceWindow]) -> None:
        msg: str = f"Unsupported PriceWindow {actual.name}. OSRS wiki api supports {[s.name for s in supported]}"
        super().__init__(msg)
