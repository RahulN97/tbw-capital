package net.runelite.client.plugins.gamedataserver.model.player;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Camera {
	private int x;
	private int y;
	private int z;
	private int yaw;
	private int scale;
}
