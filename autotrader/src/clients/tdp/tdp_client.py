from typing import Any, Dict

from core.clients.base_client import BaseClient
from requests import Session

from clients.tdp.exceptions import TdpApiError


class TdpClient(BaseClient):

    def __init__(self) -> None:
        self.session: Session = Session()
        self.url: str = f"http://localhost:{}"
        super().__init__()

    def establish_connection(self) -> None:
        data: Dict[str, Any] = self.session.get("/health")
        if data["health"] != "healthy":
            raise TdpApiError(f"Trade Data Platform health status: {data['health']}")
