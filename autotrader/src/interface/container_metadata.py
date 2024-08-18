from dataclasses import dataclass
from typing import Tuple


@dataclass(frozen=True)
class ContainerMetadata:
    slot_index_range: Tuple[int, int]
    num_cols: int
    x_offset: int
    y_offset: int
