package net.runelite.client.plugins.gamedataserver.model.exchange;

import net.runelite.api.GrandExchangeOfferState;

public enum ExchangeOrderState {
	EMPTY,
	CANCELLED_BUY,
	BUYING,
	BOUGHT,
	CANCELLED_SELL,
	SELLING,
	SOLD;

	public static ExchangeOrderState fromGrandExchangeState(GrandExchangeOfferState state) {
		return ExchangeOrderState.valueOf(state.name());
	}
}
