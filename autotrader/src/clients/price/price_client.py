import requests


class PriceClient:

    def __init__(self, url: str) -> None:
        self.session: requests.Session = requests.Session()
        self.url: str = url
