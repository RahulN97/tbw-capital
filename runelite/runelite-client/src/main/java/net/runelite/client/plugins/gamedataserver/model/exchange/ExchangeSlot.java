package net.runelite.client.plugins.gamedataserver.model.exchange;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class ExchangeSlot {
	private int position;
	private int itemId;
	private int price;
	private int quantityTransacted;
	private int totalQuantity;
	private ExchangeSlotState state;

	public static ExchangeSlot asEmpty(int position) {
		return ExchangeSlot.builder()
			.position(position)
			.itemId(-1)
			.price(-1)
			.quantityTransacted(-1)
			.totalQuantity(-1)
			.state(ExchangeSlotState.EMPTY)
			.build();
	}
}
