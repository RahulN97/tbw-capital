package net.runelite.client.plugins.gamedataserver.model.config;

import lombok.Data;
import lombok.experimental.SuperBuilder;

@SuperBuilder
@Data
public abstract class StratConfig {
	private boolean activated;
	private int waitDuration;
	private int maxOfferTime;
}
