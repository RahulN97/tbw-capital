package net.runelite.client.plugins.gamedataserver.model;

import lombok.Builder;
import lombok.Data;

import java.time.Instant;

@Builder
@Data
public class GameDataSnapshot {
	private Exchange exchange;
	private Inventory inventory;
	private Player player;
	private Instant creationTime;
}
