package net.runelite.client.plugins.gamedataserver.model;

import lombok.Builder;
import lombok.Data;
import net.runelite.client.plugins.gamedataserver.model.chat.ChatBox;
import net.runelite.client.plugins.gamedataserver.model.exchange.Exchange;
import net.runelite.client.plugins.gamedataserver.model.inventory.Inventory;
import net.runelite.client.plugins.gamedataserver.model.player.Player;

import java.time.Instant;

@Builder
@Data
public class GameDataSnapshot {
	private Session session;
	private Exchange exchange;
	private Inventory inventory;
	private Player player;
	private ChatBox chatBox;
	private Instant creationTime;
}
