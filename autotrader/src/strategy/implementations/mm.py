from typing import Dict, List, Optional

from core.clients.gds.models.config.strat_config import MMStratConfig
from core.clients.gds.models.config.top_level_config import TopLevelConfig
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.price.models.item_metadata import ItemMetadata
from core.clients.price.models.price_data_snapshot import PriceDataSnapshot
from core.clients.redis.redis_client import RedisClient

from strategy.action import (
    BuyAction,
    CancelBuyAction,
    CancelOrderAction,
    CancelSellAction,
    OrderAction,
    SellAction,
)
from strategy.strategy import BaseStrategy


# def _demo(self):
#     id1: int = 561
#     name1: str = self.item_map[id1].name
#     id2: int = 556
#     name2: str = self.item_map[id2].name
#     if self.demo == 1:
#         self.demo += 1
#         return [
#             BuyAction(item_id=id1, item_name=name1, price=150, quantity=10),
#             BuyAction(item_id=id2, item_name=name2, price=10, quantity=25),
#         ]
#     if self.demo == 2:
#         self.demo += 1
#         return [
#             SellAction(item_id=id1, item_name=name1, price=100, quantity=10),
#             SellAction(item_id=id2, item_name=name2, price=20, quantity=20),
#         ]
#     if self.demo == 3:
#         self.demo += 1
#         return [CancelSellAction(ge_slot=1)]
#     return []


class MMStrategy(BaseStrategy):

    def __init__(
        self,
        redis_client: RedisClient,
        top_level_config: TopLevelConfig,
        strat_config: MMStratConfig,
        universe: Optional[List[int]],
        item_map: Dict[int, ItemMetadata],
    ) -> None:
        super().__init__(
            redis_client=redis_client,
            top_level_config=top_level_config,
            strat_config=strat_config,
            universe=universe,
            item_map=item_map,
        )
        self.items_traded: List[int] = []

    @property
    def name(self) -> str:
        return "Market Maker"

    def is_over_buy_limit(self, item_id: int) -> bool:
        pass

    def generate_cancel_orders(self, exchange: Exchange) -> List[CancelOrderAction]:
        orders: List[CancelOrderAction] = []
        for slot in exchange.slots:
            # TODO: determine if slot needs to be cancelled
            pass
        return orders

    def generate_sell_orders(self, inventory: Inventory, price_data: PriceDataSnapshot) -> List[SellAction]:
        orders: List[SellAction] = []
        for item in inventory.items:
            if item.id not in self.universe:
                continue

            # TODO: calculate sell price
            price: int = 0

            orders.append(
                SellAction(
                    item_id=item.id,
                    item_name=self.item_map[item.id].name,
                    price=price,
                    quantity=item.quantity,
                )
            )
        return orders

    def generate_buy_orders(self, inventory: Inventory, price_data: PriceDataSnapshot) -> List[BuyAction]:
        orders: List[BuyAction] = []
        for item_id in self.universe:
            if self.is_over_buy_limit(item_id):
                continue

            # TODO: calculate buy price, qty, and expected profit (based on sell price)
            price: int = 0
            quantity: int = 0
            expected_profit: int = 0

            if expected_profit < self.top_level_config.min_gp:
                continue

            orders.append(
                BuyAction(
                    item_id=item_id,
                    item_name=self.item_map[item_id].name,
                    price=price,
                    quantity=quantity,
                )
            )

        return orders

    def compute(
        self,
        exchange: Exchange,
        inventory: Inventory,
        price_data: PriceDataSnapshot,
    ) -> List[OrderAction]:
        cancels: List[CancelOrderAction] = self.generate_cancel_orders(exchange=exchange)
        sells: List[SellAction] = self.generate_sell_orders(inventory=inventory, price_data=price_data)
        buys: List[BuyAction] = self.generate_buy_orders(inventory=inventory, price_data=price_data)

        orders: List[OrderAction] = self.extract_executable_orders(
            exchange=exchange,
            cancels=cancels,
            sells=sells,
            buys=buys,
        )
        self.validate_orders(orders)
        return orders
