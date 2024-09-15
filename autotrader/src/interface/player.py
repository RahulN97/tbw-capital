from core.clients.gds.gds_client import GdsClient
from core.clients.gds.models.player.camera import Camera
from core.clients.gds.models.player.player_location import PlayerLocation
from core.clients.gds.models.player.player_state import PlayerState
from core.logger import logger

from interface.controller import Controller
from interface.exceptions import UnexpectedPlayerStateError


class Player:

    EXPECTED_PLAYER_STATE: PlayerState = PlayerState(
        camera=Camera(z=-878, yaw=0, scale=3600),
        location=PlayerLocation(x=3165, y=3487),
    )
    DOWN_DURATION_SECS: int = 3

    def __init__(self, controller: Controller, gds_client: GdsClient) -> None:
        self.controller: Controller = controller
        self.gds_client: GdsClient = gds_client

    def _is_player_ready(self) -> bool:
        player_state: PlayerState = self.gds_client.get_player_data()
        return (
            player_state.location == self.EXPECTED_PLAYER_STATE.location
            and player_state.camera.z == self.EXPECTED_PLAYER_STATE.camera.z
            and player_state.camera.yaw == self.EXPECTED_PLAYER_STATE.camera.yaw
            and player_state.camera.scale > self.EXPECTED_PLAYER_STATE.camera.scale
        )

    def prepare(self) -> None:
        if self._is_player_ready():
            return

        logger.info("Preparing player at exchange")
        # TODO: walk to ge tile if needed
        self.controller.click_location("compass")
        self.controller.scroll_full_zoom()
        self.controller.hold("down", self.DOWN_DURATION_SECS)
        if not self._is_player_ready():
            player_state: PlayerState = self.gds_client.get_player_data()
            raise UnexpectedPlayerStateError(
                player_state=player_state,
                expected_player_state=self.EXPECTED_PLAYER_STATE,
            )
