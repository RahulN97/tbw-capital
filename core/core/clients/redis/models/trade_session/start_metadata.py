from dataclasses import dataclass
from typing import Dict


@dataclass
class StartMetadata:
    start_time: float
    start_nw: int
    start_items: Dict[int, int]
