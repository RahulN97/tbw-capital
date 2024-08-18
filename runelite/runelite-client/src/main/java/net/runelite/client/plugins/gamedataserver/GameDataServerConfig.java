package net.runelite.client.plugins.gamedataserver;

import net.runelite.client.config.*;

@ConfigGroup("gamedataserver")
public interface GameDataServerConfig extends Config {
	@ConfigItem(
		keyName = "autotraderOn",
		name = "Start Autotrader",
		description = "Toggle to start/stop autotrader",
		position = 0
	)
	default boolean autotraderOn() {
		return false;
	}

	@ConfigSection(
		name = "Top Level",
		description = "Shared configs for all strategies in autotrader",
		position = 1
	)
	String topLevelSection = "Top Level";

	@ConfigSection(
		name = "Market Maker",
		description = "Configs for market maker strategy",
		position = 2
	)
	String mmSection = "Market Maker";

	@ConfigItem(
		position = 1,
		keyName = "minGp",
		name = "Min GP",
		description = "Minimum GP a trade must make in order for it to be considered",
		section = topLevelSection
	)
    default int minGp() {
		return 1000;
	}

	@ConfigItem(
		keyName = "mmActivated",
		name = "Activate MM Strategy",
		description = "Turns on the MM strategy in autotrader",
		position = 2,
		section = mmSection
	)
	default boolean mmActivated()
	{
		return true;
	}

	@ConfigItem(
		keyName = "mmWaitDuration",
		name = "Wait Duration",
		description = "Amount of seconds to wait before recomputing strategy",
		position = 3,
		section = mmSection
	)
	@Units(Units.SECONDS)
	default int mmWaitDuration()
	{
		return 30;
	}

	@ConfigItem(
		position = 4,
		keyName = "maxOfferTime",
		name = "Max Offer Time",
		description = "Maximum amount of time to let an offer sit in the exchange in minutes",
		section = mmSection
	)
	@Units(Units.SECONDS)
	default int maxOfferTime() {
		return 3600;
	}
}
