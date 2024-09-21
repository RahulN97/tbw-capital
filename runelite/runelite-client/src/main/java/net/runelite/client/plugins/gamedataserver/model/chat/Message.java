package net.runelite.client.plugins.gamedataserver.model.chat;

import lombok.Builder;
import lombok.Data;

@Builder
@Data
public class Message {
	private String content;
	private String sender;
	private int timestamp;
}
