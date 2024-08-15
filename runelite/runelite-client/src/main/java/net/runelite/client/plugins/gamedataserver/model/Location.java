package net.runelite.client.plugins.gamedataserver.model;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Location {
	private int x;
	private int y;
}
