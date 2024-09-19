package net.runelite.client.plugins.gamedataserver.model;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Session {
	private String id;
	private long startTime;
	private String playerName;
	private boolean isF2p;
}
