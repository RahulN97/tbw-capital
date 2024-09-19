from typing import Dict

from core.clients.service import HttpMethod, ServiceCall
from core.clients.tdp.stubs.limits import GetBuyLimitsRequest, GetBuyLimitsResponse, UpdateBuyLimitsRequest
from core.clients.tdp.stubs.metrics import GetNetWorthRequest, GetNetWorthResponse, GetPnlRequest, GetPnlResponse
from core.clients.tdp.stubs.session import (
    CreateTradeSessionRequest,
    CreateTradeSessionResponse,
    CreateTradesRequest,
    CreateTradesResponse,
    GetOrdersRequest,
    GetOrdersResponse,
    GetTradeSessionRequest,
    GetTradeSessionResponse,
    GetTradesRequest,
    GetTradesResponse,
    UpdateOrdersRequest,
    UpdateTradeSessionRequest,
)


SERVICE_DEFINITIONS: Dict[str, ServiceCall] = {
    "GetBuyLimits": ServiceCall(
        endpoint="/limits",
        http_method=HttpMethod.GET,
        request_type=GetBuyLimitsRequest,
        response_type=GetBuyLimitsResponse,
    ),
    "UpdateBuyLimits": ServiceCall(
        endpoint="/limits",
        http_method=HttpMethod.POST,
        request_type=UpdateBuyLimitsRequest,
        response_type=None,
    ),
    "GetTradeSession": ServiceCall(
        endpoint="/session",
        http_method=HttpMethod.GET,
        request_type=GetTradeSessionRequest,
        response_type=GetTradeSessionResponse,
    ),
    "CreateTradeSession": ServiceCall(
        endpoint="/session",
        http_method=HttpMethod.POST,
        request_type=CreateTradeSessionRequest,
        response_type=CreateTradeSessionResponse,
    ),
    "UpdateTradeSession": ServiceCall(
        endpoint="/session",
        http_method=HttpMethod.PUT,
        request_type=UpdateTradeSessionRequest,
        response_type=None,
    ),
    "GetOrders": ServiceCall(
        endpoint="/session/orders",
        http_method=HttpMethod.GET,
        request_type=GetOrdersRequest,
        response_type=GetOrdersResponse,
    ),
    "UpdateOrders": ServiceCall(
        endpoint="/session/orders",
        http_method=HttpMethod.PUT,
        request_type=UpdateOrdersRequest,
        response_type=None,
    ),
    "GetTrades": ServiceCall(
        endpoint="/session/trades",
        http_method=HttpMethod.GET,
        request_type=GetTradesRequest,
        response_type=GetTradesResponse,
    ),
    "CreateTrades": ServiceCall(
        endpoint="/session/trades",
        http_method=HttpMethod.POST,
        request_type=CreateTradesRequest,
        response_type=CreateTradesResponse,
    ),
    "GetPnl": ServiceCall(
        endpoint="/metrics/pnl",
        http_method=HttpMethod.GET,
        request_type=GetPnlRequest,
        response_type=GetPnlResponse,
    ),
    "GetNetWorth": ServiceCall(
        endpoint="/metrics/nw",
        http_method=HttpMethod.GET,
        request_type=GetNetWorthRequest,
        response_type=GetNetWorthResponse,
    ),
}
