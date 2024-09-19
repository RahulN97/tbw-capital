package net.runelite.client.plugins.gamedataserver.model.player;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Player {
	private boolean loggedIn;
	private Location location;
	private Camera camera;
}
