package net.runelite.client.plugins.gamedataserver.model;

import lombok.Builder;
import lombok.Data;
import lombok.Singular;

import java.util.List;

@Builder
@Data
public class Inventory {
	@Singular
	private List<Item> items;
}
