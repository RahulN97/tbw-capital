from dataclasses import dataclass
from typing import Dict, Set

from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.price.models.price import LatestPrice


@dataclass
class PnlCalcData:
    trade_ids: Dict[str, Set[str]]
    inv_snapshot: Inventory
    exchange_snapshot: Exchange
    prices_snapshot: Dict[int, LatestPrice]


@dataclass
class PnlSnapshot:
    strat_pnl: Dict[str, int]
    calc_data: PnlCalcData
    update_time: float
