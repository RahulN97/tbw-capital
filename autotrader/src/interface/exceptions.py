from typing import Tuple

from core.clients.gds.models.player.player_state import PlayerState


class MissingCoordinatesError(Exception):
    def __init__(self, name: str) -> None:
        msg: str = f"Coordinates for {name} not found."
        super().__init__(msg)


class SlotIndexError(Exception):
    def __init__(self, actual: int, expected_range: Tuple[int, int]) -> None:
        msg: str = f"Cannot process slot index: {actual}. Expected range: {list(expected_range)}."
        super().__init__(msg)


class UnexpectedPlayerStateError(Exception):
    def __init__(self, player_state: PlayerState, expected_player_state: PlayerState) -> None:
        msg: str = f"Player is in unexpected state: {player_state}; expected player state: {expected_player_state}."
        super().__init__(msg)
