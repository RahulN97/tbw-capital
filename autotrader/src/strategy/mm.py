from typing import Dict, List, Optional

from core.clients.gds.models.config.strat_config import MMStratConfig
from core.clients.gds.models.config.top_level_config import TopLevelConfig
from core.clients.gds.models.exchange.exchange import Exchange
from core.clients.gds.models.inventory.inventory import Inventory
from core.clients.redis.redis_client import RedisClient

from clients.price.models.item_metadata import ItemMetadata
from clients.price.models.price_data_snapshot import PriceDataSnapshot
from models.order import BuyOrder, CancelOrder, OrderAction, SellOrder
from strategy.strategy import BaseStrategy


# for demo
# item_id: int = 561
# item_name: str = self.item_map[item_id]
# return [
#     BuyOrder(item_id=item_id, item_name=item_name, price=150, quantity=10),
#     SellOrder(item_id=item_id, item_name=item_name, price=160, quantity=5),
#     CancelOrder(ge_slot=0),
#     SellOrder(item_id=item_id, item_name=item_name, price=100, quantity=10),
# ]


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

    def generate_cancel_orders(self, exchange: Exchange) -> List[CancelOrder]:
        orders: List[CancelOrder] = []
        for slot in exchange.slots:
            # TODO: determine if slot needs to be cancelled
            pass
        return orders

    def generate_sell_orders(self, inventory: Inventory, price_data: PriceDataSnapshot) -> List[SellOrder]:
        orders: List[SellOrder] = []
        for item in inventory.items:
            if item.id not in self.universe:
                continue

            # TODO: calculate sell price
            price: int = 0

            orders.append(
                SellOrder(
                    item_id=item.id,
                    item_name=self.item_map[item.id].name,
                    price=price,
                    quantity=item.quantity,
                )
            )
        return orders

    def generate_buy_orders(self, inventory: Inventory, price_data: PriceDataSnapshot) -> List[BuyOrder]:
        orders: List[BuyOrder] = []
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
                BuyOrder(
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
        cancels: List[CancelOrder] = self.generate_cancel_orders(exchange=exchange)
        sells: List[SellOrder] = self.generate_sell_orders(inventory=inventory, price_data=price_data)
        buys: List[BuyOrder] = self.generate_buy_orders(inventory=inventory, price_data=price_data)

        orders: List[OrderAction] = self.extract_executable_orders(
            exchange=exchange,
            cancels=cancels,
            sells=sells,
            buys=buys,
        )
        self.validate_orders(orders)
        return orders
        return orders
