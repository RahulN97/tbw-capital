package net.runelite.client.plugins.gamedataserver.model;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Player {
	private Location location;
	private Camera camera;
}
