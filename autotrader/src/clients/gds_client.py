import requests


class GdsClient:

    def __init__(self, gds_host: str, gds_port: int) -> None:
        self.session: requests.Session = requests.Session()
        self.url: str = f"http://{gds_host}:{gds_port}"
