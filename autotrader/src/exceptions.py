from core.clients.gds.models.player.player_state import PlayerState


class UnexpectedPlayerStateError(Exception):
    def __init__(self, player_state: PlayerState, expected_player_state: PlayerState) -> None:
        msg: str = f"Player is in unexpected state: {player_state}; expected player state: {expected_player_state}."
        super().__init__(msg)


class UnsupportedOrderActionError(Exception):
    def __init__(self, actual: str, expected: str) -> None:
        msg: str = f"Unsupported OrderAction type: {actual}. Expected type {expected}"
        super().__init__(msg)


class MissingInventoryItemError(Exception):
    def __init__(self, item_id: int) -> None:
        msg: str = f"Missing item id {item_id} in inventory"
        super().__init__(msg)


class NoAvailableGeSlotError(Exception):
    def __init__(self) -> None:
        super().__init__("No available GE slots to execute order.")
