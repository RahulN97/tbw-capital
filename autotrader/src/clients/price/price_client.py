from typing import Any, Dict, FrozenSet, Optional

import requests
from requests import Response, Session

from clients.price.exceptions import PriceApiError, UnsupportedPriceWindowError
from clients.price.models.price import AvgPrice, LatestPrice
from clients.price.models.price_window import PriceWindow


class PriceClient:

    OSRS_WIKI_URL: str = "https://prices.runescape.wiki/api/v1/osrs"
    HEADERS: Dict[str, str] = {"User-Agent": "tbw-capital@gmail.com"}

    SUPPORTED_PRICE_WINDOWS: FrozenSet[PriceWindow] = frozenset((PriceWindow.AVG_5M, PriceWindow.AVG_1H))

    def __init__(self) -> None:
        self.session: Session = requests.Session()
        self.url: str = self.OSRS_WIKI_URL

    def get(self, endpoint: str) -> Dict[str, Any]:
        resp: Response = self.session.get(url=self.url + endpoint, headers=self.HEADERS)
        if resp.status_code != 200:
            raise PriceApiError(resp.text)
        return resp.json()

    def get_item_mapping(self, filter_ids: Optional[FrozenSet[int]] = None) -> Dict[int, str]:
        data: Dict[str, Any] = self.get("/mapping")
        if filter_ids is None:
            return {d["id"]: d["name"] for d in data}
        return {d["id"]: d["name"] for d in data if d["id"] in filter_ids}

    def get_latest_prices(self, filter_ids: Optional[FrozenSet[int]] = None) -> Dict[int, LatestPrice]:
        resp_data: Dict[str, Any] = self.get("/latest")
        data: Dict[int, Dict[str, int]] = resp_data["data"]

        price_map: Dict[int, LatestPrice] = {}
        for item_id, price_data in data.items():
            if filter_ids is not None and item_id not in filter_ids:
                continue
            price_map[item_id] = LatestPrice(
                low_price=price_data["low"],
                high_price=price_data["high"],
                low_time=price_data["lowTime"],
                high_time=price_data["highTime"],
            )

        return price_map

    def get_avg_prices(self, window: PriceWindow, filter_ids: Optional[FrozenSet[int]] = None) -> Dict[int, AvgPrice]:
        if window == PriceWindow.AVG_5M:
            endpoint: str = "/5m"
        elif window == PriceWindow.AVG_1H:
            endpoint: str = "/1h"
        else:
            raise UnsupportedPriceWindowError(actual=window, supported=self.SUPPORTED_PRICE_WINDOWS)

        resp_data: Dict[str, Any] = self.get(endpoint)
        data: Dict[int, Dict[str, int]] = resp_data["data"]

        price_map: Dict[int, AvgPrice] = {}
        for item_id, price_data in data.items():
            if filter_ids is not None and item_id not in filter_ids:
                continue
            price_map[item_id] = AvgPrice(
                low_price=price_data["avgLowPrice"],
                high_price=price_data["avgHighPrice"],
                low_volume=price_data["lowPriceVolume"],
                high_volume=price_data["highPriceVolume"],
                price_window=window,
            )

        return price_map
