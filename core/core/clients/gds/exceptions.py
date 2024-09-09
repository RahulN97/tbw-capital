class GdsApiError(Exception):
    def __init__(self, error_msg: str) -> None:
        msg: str = f"GDS API call failed with error: {error_msg}."
        super().__init__(msg)


class GdsUnexpectedResponseError(Exception):
    def __init__(self, val: str, field: str, endpoint: str) -> None:
        msg: str = f"GDS API returned unexpected response value {val} for field {field} from endpoint {endpoint}"
        super().__init__(msg)
