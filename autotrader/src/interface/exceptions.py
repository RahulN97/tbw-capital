class MissingCoordinatesError(Exception):
    def __init__(self, name: str) -> None:
        msg: str = f"Coordinates for {name} not found."
        super().__init__(msg)
