package net.runelite.client.plugins.gamedataserver.model.exchange;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class ExchangeOrder {
	private int position;
	private int itemId;
	private int price;
	private int quantityTransacted;
	private int totalQuantity;
	private ExchangeOrderState state;

	public static ExchangeOrder asEmpty(int position) {
		return ExchangeOrder.builder()
			.position(position)
			.itemId(-1)
			.price(-1)
			.quantityTransacted(-1)
			.totalQuantity(-1)
			.state(ExchangeOrderState.EMPTY)
			.build();
	}
}
