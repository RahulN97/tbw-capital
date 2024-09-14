class TdpApiError(Exception):
    def __init__(self, error_msg: str) -> None:
        msg: str = f"TDP API call failed with error: {error_msg}."
        super().__init__(msg)


class UnsupportedServiceCall(Exception):
    def __init__(self, call: str) -> None:
        super().__init__(f"No service call definition found for {call}")
