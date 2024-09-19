from dataclasses import dataclass
from typing import List

from core.clients.redis.models.pnl.pnl_snapshot import PnlSnapshot
from core.redis_object import RedisObject


@dataclass
class Pnl(RedisObject):
    session_id: str
    total_pnl: int
    pnl_snapshots: List[PnlSnapshot]
    update_time: float
