package net.runelite.client.plugins.gamedataserver.model.config;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Builder
@Data
public class LiveConfig {
	private boolean autotraderOn;
	private TopLevelConfig topLevelConfig;
	private List<StratConfig> stratConfigs;
}
