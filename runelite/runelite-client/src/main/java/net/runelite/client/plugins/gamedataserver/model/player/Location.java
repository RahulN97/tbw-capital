package net.runelite.client.plugins.gamedataserver.model.player;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Location {
	private int x;
	private int y;
}
