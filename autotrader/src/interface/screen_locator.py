import json
import random
from typing import Any, Dict, List, Tuple

from interface.container_metadata import ContainerMetadata
from interface.exceptions import MissingCoordinatesError, SlotIndexError
from models.location import Location


class ScreenLocator:

    GE_CONTAINER_METADATA: ContainerMetadata = ContainerMetadata(
        slot_index_range=(0, 7),
        num_cols=4,
        x_offset=117,
        y_offset=120,
    )

    INV_CONTAINER_METADATA: ContainerMetadata = ContainerMetadata(
        slot_index_range=(0, 27),
        num_cols=4,
        x_offset=42,
        y_offset=36,
    )

    def __init__(self, randomize: bool) -> None:
        self.location_map: Dict[str, Location] = self.build_location_map()
        self.randomize = randomize

    @staticmethod
    def build_location_map() -> Dict[str, Location]:
        with open("data/locations.json", "r") as f:
            locations: List[Dict[str, Any]] = json.load(f)["locations"]
        return {
            loc["name"]: Location(
                x=loc["coordinates"]["x"],
                y=loc["coordinates"]["y"],
                x_jitter=loc["jitter"]["x"],
                y_jitter=loc["jitter"]["y"],
            )
            for loc in locations
        }

    @staticmethod
    def _is_slot_out_of_bounds(slot_num: int, slot_range: Tuple[int, int]) -> bool:
        return slot_num < slot_range[0] or slot_num > slot_range[1]

    @staticmethod
    def _get_slot_coords(
        slot_num: int,
        base_x: int,
        base_y: int,
        container: ContainerMetadata,
    ) -> Tuple[int, int]:
        row: int = slot_num // container.num_cols
        col: int = slot_num % container.num_cols

        x: int = base_x + (col * container.x_offset)
        y: int = base_y + (row * container.y_offset)

        return x, y

    def get_coords(self, name: str) -> Tuple[int, int]:
        try:
            loc: Location = self.location_map[name]
        except KeyError:
            raise MissingCoordinatesError(name)

        if not self.randomize:
            return loc.x, loc.y
        return (
            random.randint(loc.x - loc.x_jitter, loc.x + loc.x_jitter),
            random.randint(loc.y - loc.y_jitter, loc.y + loc.y_jitter),
        )

    def get_inv_slot_coords(self, slot_num: int) -> Tuple[int, int]:
        container: ContainerMetadata = self.INV_CONTAINER_METADATA
        if self._is_slot_out_of_bounds(slot_num=slot_num, slot_range=container.slot_index_range):
            raise SlotIndexError(actual=slot_num, expected_range=container.slot_index_range)

        base_x, base_y = self.get_coords("inv_slot")

        return self._get_slot_coords(
            slot_num=slot_num,
            base_x=base_x,
            base_y=base_y,
            container=container,
        )

    def get_ge_slot_coords(self, slot_num: int) -> Tuple[int, int]:
        container: ContainerMetadata = self.GE_CONTAINER_METADATA
        if self._is_slot_out_of_bounds(slot_num=slot_num, slot_range=container.slot_index_range):
            raise SlotIndexError(actual=slot_num, expected_range=container.slot_index_range)

        base_x, base_y = self.get_coords("ge_slot")

        return self._get_slot_coords(
            slot_num=slot_num,
            base_x=base_x,
            base_y=base_y,
            container=container,
        )
