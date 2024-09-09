from dataclasses import dataclass

from core.clients.gds.models.player.camera import Camera
from core.clients.gds.models.player.player_location import PlayerLocation


@dataclass
class PlayerState:
    camera: Camera
    location: PlayerLocation
