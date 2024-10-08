class UnsupportedStratError(Exception):
    def __init__(self, strat_type: str) -> None:
        msg: str = f"Unsupported strat type: {strat_type}"
        super().__init__(msg)


class MissingGpError(Exception):
    def __init__(self) -> None:
        super().__init__("No cash stack in inventory")
