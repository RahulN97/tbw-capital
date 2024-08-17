package net.runelite.client.plugins.gamedataserver.model.exchange;

import lombok.Builder;
import lombok.Data;
import lombok.Singular;

import java.util.List;

@Builder
@Data
public class Exchange {
	@Singular
	private List<ExchangeOrder> orders;
}
