from core.clients.redis.models.pnl.pnl import Pnl
from core.clients.service import ApiBaseModel


class MetricsRequest(ApiBaseModel):
    session_id: str


class GetPnlRequest(MetricsRequest):
    pass


class GetPnlResponse(ApiBaseModel):
    pnl: Pnl


class GetNetWorthRequest(MetricsRequest):
    pass


class GetNetWorthResponse(ApiBaseModel):
    nw: int
