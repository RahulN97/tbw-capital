package net.runelite.client.plugins.gamedataserver.model.exchange;

import net.runelite.api.GrandExchangeOfferState;

public enum ExchangeSlotState {
	EMPTY,
	CANCELLED_BUY,
	BUYING,
	BOUGHT,
	CANCELLED_SELL,
	SELLING,
	SOLD;

	public static ExchangeSlotState fromGrandExchangeOfferState(GrandExchangeOfferState state) {
		return ExchangeSlotState.valueOf(state.name());
	}
}
