from dataclasses import dataclass
from typing import Dict, List, Type

from core.clients.price.models.price import AvgPrice, LatestPrice


@dataclass(frozen=True)
class PriceDataSnapshot:
    latest_map: Dict[int, LatestPrice]
    avg_5m_map: Dict[int, AvgPrice]
    avg_1h_map: Dict[int, AvgPrice]

    @classmethod
    def filter_by_items(
        cls: Type["PriceDataSnapshot"],
        full_snapshot: "PriceDataSnapshot",
        item_ids: List[int],
    ) -> "PriceDataSnapshot":
        return cls(
            latest_map={i: p for i, p in full_snapshot.latest_map.items() if i in item_ids},
            avg_5m_map={i: p for i, p in full_snapshot.avg_5m_map.items() if i in item_ids},
            avg_1h_map={i: p for i, p in full_snapshot.avg_1h_map.items() if i in item_ids},
        )
