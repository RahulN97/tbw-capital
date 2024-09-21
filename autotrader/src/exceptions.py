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


class PlayerStateError(Exception):
    def __init__(self, msg) -> None:
        super().__init__(msg)
