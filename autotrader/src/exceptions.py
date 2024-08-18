from clients.gds.models.player.player_state import PlayerState


class UnexpectedPlayerStateError(Exception):
    def __init__(self, player_state: PlayerState, expected_player_state: PlayerState) -> None:
        msg: str = f"Player is in unexpected state: {player_state}; expected player state: {expected_player_state}."
        super().__init__(msg)


class UnsupportedOrderAction(Exception):
    def __init__(self, actual: str, expected: str) -> None:
        msg: str = f"Unsupported OrderAction type: {actual}. Expected type {expected}"
        super().__init__(msg)
