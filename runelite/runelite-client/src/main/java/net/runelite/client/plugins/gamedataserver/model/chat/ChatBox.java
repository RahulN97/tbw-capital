package net.runelite.client.plugins.gamedataserver.model.chat;

import lombok.Builder;
import lombok.Data;

import java.util.List;

@Builder
@Data
public class ChatBox {
	List<Message> messages;
}
