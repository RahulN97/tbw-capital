from functools import cached_property
from typing import Any, Dict, List

from requests import Response, Session

from core.clients.base_client import BaseClient
from core.clients.gds.exceptions import GdsApiError, GdsUnexpectedResponseError
from core.clients.gds.models.chat.chat_box import ChatBox
from core.clients.gds.models.chat.message import Message
from core.clients.gds.models.config.live_config import LiveConfig
from core.clients.gds.models.config.strat_config import MMStratConfig, StratConfig
from core.clients.gds.models.config.top_level_config import TopLevelConfig
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.exchange.exchange_slot import ExchangeSlot
from core.clients.gds.models.exchange.exchange_slot_state import ExchangeSlotState
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.gds.models.inventory.item import Item
from core.clients.gds.models.player.camera import Camera
from core.clients.gds.models.player.player_location import PlayerLocation
from core.clients.gds.models.player.player_state import PlayerState
from core.clients.gds.models.session_metadata import SessionMetadata


class GdsClient(BaseClient):

    MAX_F2P_EXCHANGE_SLOTS: int = 3

    def __init__(self, host: str, port: int) -> None:
        self.session: Session = Session()
        self.url: str = f"http://{host}:{port}"

    def establish_connection(self) -> None:
        data: Dict[str, Any] = self.get("/health")
        if data["health"] != "healthy":
            raise GdsApiError(f"RuneLite server health status: {data['health']}")

    @cached_property
    def session_metadata(self) -> SessionMetadata:
        endpoint: str = "/session"
        data: Dict[str, Any] = self.get(endpoint)
        return SessionMetadata(
            id=data["id"],
            start_time=data["startTime"],
            player_name=data["playerName"],
            is_f2p=data["isF2p"],
        )

    def get(self, endpoint: str) -> Dict[str, Any]:
        resp: Response = self.session.get(url=self.url + endpoint)
        if resp.status_code != 200:
            raise GdsApiError(resp.text)
        return resp.json()

    def get_live_config(self) -> LiveConfig:
        endpoint: str = "/config"
        data: Dict[str, Any] = self.get(endpoint)

        top_level_config: TopLevelConfig = TopLevelConfig(min_gp=data["topLevelConfig"]["minGp"])

        strat_configs: List[StratConfig] = []
        for config in data["stratConfigs"]:
            if config["type"] == "mmConfig":
                strat_configs.append(
                    MMStratConfig(
                        activated=config["activated"],
                        wait_duration=config["waitDuration"],
                        max_offer_time=config["maxOfferTime"],
                    )
                )
            else:
                raise GdsUnexpectedResponseError(
                    val=config["type"],
                    field="stratConfig type",
                    endpoint=endpoint,
                )

        return LiveConfig(
            trading_enabled=data["autotraderOn"],
            top_level_config=top_level_config,
            strat_configs=strat_configs,
        )

    def get_exchange(self) -> Exchange:
        endpoint: str = "/exchange"
        data: Dict[str, Any] = self.get(endpoint)

        slots: List[ExchangeSlot] = [
            ExchangeSlot(
                position=slot["position"],
                item_id=slot["itemId"],
                price=slot["price"],
                quantity_transacted=slot["quantityTransacted"],
                total_quantity=slot["totalQuantity"],
                state=ExchangeSlotState.from_str(slot["state"]),
            )
            for slot in data["slots"]
        ]
        return Exchange(slots=slots[: self.MAX_F2P_EXCHANGE_SLOTS] if self.session_metadata.is_f2p else slots)

    def get_inventory(self) -> Inventory:
        endpoint: str = "/inventory"
        data: Dict[str, Any] = self.get(endpoint)

        items: List[Item] = [
            Item(
                id=item["id"],
                quantity=item["quantity"],
                inventory_position=item["inventoryPosition"],
            )
            for item in data["items"]
        ]
        return Inventory(items=items)

    def get_player_data(self) -> PlayerState:
        endpoint: str = "/player"
        data: Dict[str, Any] = self.get(endpoint)

        camera_data: Dict[str, int] = data["camera"]
        camera: Camera = Camera(
            z=camera_data["z"],
            yaw=camera_data["yaw"],
            scale=camera_data["scale"],
        )

        location_data: Dict[str, int] = data["location"]
        location: PlayerLocation = PlayerLocation(x=location_data["x"], y=location_data["y"])

        return PlayerState(logged_in=data["loggedIn"], camera=camera, location=location)

    def get_chat_box(self) -> ChatBox:
        endpoint: str = "/chat"
        data: Dict[str, Any] = self.get(endpoint)

        messages: List[Message] = [
            Message(content=msg["content"], sender=msg["sender"], time=msg["time"]) for msg in data["messages"]
        ]
        return ChatBox(messages=messages)
