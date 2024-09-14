from typing import Any, Callable, Dict, List, Optional

from requests import Response, Session

from core.clients.base_client import BaseClient
from core.clients.redis.models.buy_limit.buy_limit import BuyLimit
from core.clients.redis.models.trade_session.order import Order
from core.clients.redis.models.trade_session.trade import Trade
from core.clients.redis.models.trade_session.trade_session import TradeSession
from core.clients.service import ApiBaseModel, ServiceCall
from core.clients.tdp.exceptions import TdpApiError, UnsupportedServiceCall
from core.clients.tdp.models.item_container import ItemContainer
from core.clients.tdp.stubs import SERVICE_DEFINITIONS
from core.clients.tdp.stubs.limits import GetBuyLimitsRequest, GetBuyLimitsResponse, UpdateBuyLimitsRequest
from core.clients.tdp.stubs.session import (
    CreateTradeSessionRequest,
    GetOrdersRequest,
    GetOrdersResponse,
    GetTradeSessionRequest,
    GetTradeSessionResponse,
    GetTradesRequest,
    GetTradesResponse,
    UpdateOrdersRequest,
    UpdateTradesRequest,
    UpdateTradesResponse,
)
from core.logger import logger


class TdpClient(BaseClient):

    HEADERS: Dict[str, str] = {"Content-Type": "application/json"}

    def __init__(self, host: str, port: int) -> None:
        self.session: Session = Session()
        self.url: str = f"http://{host}:{port}"
        super().__init__()

    def establish_connection(self) -> None:
        resp: Response = self.session.get(f"{self.url}/health")
        if resp.status_code != 200:
            raise TdpApiError(resp.text)

        data: Dict[str, Any] = resp.json()
        if data["status"] != "healthy":
            raise TdpApiError(f"Trade Data Platform health status: {data['health']}")

    def invoke(self, call: str, request: ApiBaseModel) -> Optional[ApiBaseModel]:
        try:
            service_call: ServiceCall = SERVICE_DEFINITIONS[call]
        except KeyError:
            raise UnsupportedServiceCall(call=call)

        url: str = self.url + service_call.endpoint
        data: Dict[str, Any] = request.model_dump()
        session_method: Callable = getattr(self.session, service_call.http_method.name.lower())

        logger.info(f"Processing {call} - issuing {service_call.http_method.name} request to {service_call.endpoint}")
        resp: Response = session_method(url=url, json=data, headers=self.HEADERS)
        if resp.status_code != 200:
            raise TdpApiError(resp.text)

        if service_call.response_type is not None:
            return service_call.response_type(**resp.json())

    def get_limits(self, container: ItemContainer, item_ids: Optional[List[int]] = None) -> Dict[int, BuyLimit]:
        req: GetBuyLimitsRequest = GetBuyLimitsRequest(container=container, item_ids=item_ids)
        resp: GetBuyLimitsResponse = self.invoke("GetBuyLimits", req)
        return resp.buy_limits

    def update_limits(self, cur_time: float) -> None:
        req: UpdateBuyLimitsRequest = UpdateBuyLimitsRequest(time=cur_time)
        self.invoke("UpdateBuyLimits", req)

    def get_trade_session(self, session_id: str) -> TradeSession:
        req: GetTradeSessionRequest = GetTradeSessionRequest(session_id=session_id)
        resp: GetTradeSessionResponse = self.invoke("GetTradeSession", req)
        return resp.trade_session

    def save_trade_session(self, trade_session: TradeSession) -> None:
        req: CreateTradeSessionRequest = CreateTradeSessionRequest(
            session_id=trade_session.session_id,
            trade_session=trade_session,
        )
        self.invoke("CreateTradeSession", req)

    def get_orders(self, session_id: str, strats: Optional[List[str]] = None) -> Dict[str, List[Order]]:
        req: GetOrdersRequest = GetOrdersRequest(session_id=session_id, strats=strats)
        resp: GetOrdersResponse = self.invoke("GetOrders", req)
        return resp.orders

    def save_orders(self, session_id: str, orders: List[Order]) -> None:
        req: UpdateOrdersRequest = UpdateOrdersRequest(session_id=session_id, orders=orders)
        self.invoke("UpdateOrders", req)

    def get_trades(self, session_id: str, strats: Optional[List[str]] = None) -> Dict[str, List[Trade]]:
        req: GetTradesRequest = GetTradesRequest(session_id=session_id, strats=strats)
        resp: GetTradesResponse = self.invoke("GetTrades", req)
        return resp.trades

    def book_trades(self, session_id: str, calc_cycle: int, time: Optional[float] = None) -> List[Trade]:
        req: UpdateTradesRequest = UpdateTradesRequest(session_id=session_id, calc_cycle=calc_cycle, time=time)
        resp: UpdateTradesResponse = self.invoke("UpdateTrades", req)
        return resp.trades
