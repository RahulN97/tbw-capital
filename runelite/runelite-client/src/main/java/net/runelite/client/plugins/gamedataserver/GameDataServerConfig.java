package net.runelite.client.plugins.gamedataserver;

import net.runelite.client.config.Config;
import net.runelite.client.config.ConfigGroup;
import net.runelite.client.config.ConfigItem;
import net.runelite.client.config.Units;

@ConfigGroup("gamedataserver")
public interface GameDataServerConfig extends Config {
	@ConfigItem(
		position = 0,
		keyName = "maxOfferTime",
		name = "Max Offer Time",
		description = "Maximum amount of time to let an offer sit in the exchange in minutes"
	)
    @Units(Units.MINUTES)
    default int maxOfferTimeMinutes() {
		return 60;
	}
}
