import json
import random
from typing import Any, Dict, List, Tuple

from interface.exceptions import MissingCoordinatesError
from models.location import Location


class ScreenLocator:

    def __init__(self, randomize: bool) -> None:
        self.location_map: Dict[str, Location] = self.build_location_map()
        self.randomize = randomize

    @staticmethod
    def build_location_map() -> Dict[str, Location]:
        with open("locations.json", "r") as f:
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
