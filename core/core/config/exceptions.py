class MissingConfigError(Exception):
    def __init__(self, missing_config: str) -> None:
        msg: str = f"Missing required config: {missing_config}."
        super().__init__(msg)
