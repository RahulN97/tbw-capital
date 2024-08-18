from typing import Tuple


class MissingCoordinatesError(Exception):
    def __init__(self, name: str) -> None:
        msg: str = f"Coordinates for {name} not found."
        super().__init__(msg)


class SlotIndexError(Exception):
    def __init__(self, actual: int, expected_range: Tuple[int, int]) -> None:
        msg: str = f"Cannot process slot index: {actual}. Expected range: {list(expected_range)}."
        super().__init__(msg)
