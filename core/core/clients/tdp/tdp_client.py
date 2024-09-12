from typing import Any, Dict, List, Optional

from requests import Response, Session

from core.clients.base_client import BaseClient
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.tdp.exceptions import TdpApiError
from core.clients.tdp.models.item_container import ItemContainer


class TdpClient(BaseClient):

    def __init__(self, host: str, port: int) -> None:
        self.session: Session = Session()
        self.url: str = f"http://{host}:{port}"
        super().__init__()

    def establish_connection(self) -> None:
        data: Dict[str, Any] = self.get("/health")
        if data["health"] != "healthy":
            raise TdpApiError(f"Trade Data Platform health status: {data['health']}")

    def get(self, endpoint: str, body: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url: str = self.url + endpoint
        resp: Response = self.session.get(url=url) if body is None else self.session.get(url=url, json=body)
        if resp.status_code != 200:
            raise TdpApiError(resp.text)
        return resp.json()

    def post(self, endpoint: str, body: Dict[str, Any]) -> Dict[str, Any]:
        resp: Response = self.session.post(url=self.url + endpoint, data=body)
        if resp.status_code != 200:
            raise TdpApiError(resp.text)
        return resp.json()

    def get_limits(
        self,
        container: ItemContainer = ItemContainer.ALL,
        item_ids: Optional[List[int]] = None,
    ) -> Dict[int, BuyLimit]:
        data: Dict[str, Any] = self.get(
            endpoint="/limits",
            body={"container": container.name, "item_ids": item_ids},
        )
        return data

    def update_limits(self, cur_time: float) -> None:
        self.post(endpoint="/limits", body={"time": cur_time})

    def save_trade_session(self, trade_session: TradeSession) -> None:
        pass

    def save_trades(self, trades: List[Trade], strat_name: str) -> None:
        pass
