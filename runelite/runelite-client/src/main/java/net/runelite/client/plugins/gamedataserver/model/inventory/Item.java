package net.runelite.client.plugins.gamedataserver.model.inventory;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Item {
	private int id;
	private int quantity;
	private int inventoryPosition;
}
