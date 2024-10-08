package net.runelite.client.plugins.gamedataserver;

import com.google.gson.Gson;
import com.google.gson.GsonBuilder;
import com.google.inject.Inject;
import com.google.inject.Provides;
import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpServer;
import lombok.extern.slf4j.Slf4j;
import net.runelite.api.*;
import net.runelite.api.coords.WorldPoint;
import net.runelite.client.config.ConfigManager;
import net.runelite.client.plugins.Plugin;
import net.runelite.client.plugins.PluginDescriptor;
import net.runelite.client.plugins.gamedataserver.model.GameDataSnapshot;
import net.runelite.client.plugins.gamedataserver.model.Session;
import net.runelite.client.plugins.gamedataserver.model.chat.ChatBox;
import net.runelite.client.plugins.gamedataserver.model.chat.Message;
import net.runelite.client.plugins.gamedataserver.model.config.LiveConfig;
import net.runelite.client.plugins.gamedataserver.model.config.MMConfig;
import net.runelite.client.plugins.gamedataserver.model.config.StratConfig;
import net.runelite.client.plugins.gamedataserver.model.config.TopLevelConfig;
import net.runelite.client.plugins.gamedataserver.model.exchange.Exchange;
import net.runelite.client.plugins.gamedataserver.model.exchange.ExchangeSlot;
import net.runelite.client.plugins.gamedataserver.model.exchange.ExchangeSlotState;
import net.runelite.client.plugins.gamedataserver.model.inventory.Inventory;
import net.runelite.client.plugins.gamedataserver.model.inventory.Item;
import net.runelite.client.plugins.gamedataserver.model.player.Camera;
import net.runelite.client.plugins.gamedataserver.model.player.Location;
import net.runelite.client.plugins.gamedataserver.model.player.Player;
import net.runelite.client.util.RuntimeTypeAdapterFactory;

import java.io.IOException;
import java.io.OutputStreamWriter;
import java.net.InetSocketAddress;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.Executors;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

@PluginDescriptor(
	name = "Game Data Server",
	description = "Serves client and game data needed for auto trading",
	loadWhenOutdated = true
)
@Slf4j
public class GameDataServerPlugin extends Plugin {
	private static final int SERVER_PORT = 19100;
	private static final int MAX_GE_SLOTS = 8;
	private static final int MAX_INVENTORY_SLOTS = 28;

	@Inject
	private Client client;

	@Inject
	private GameDataServerConfig config;
	private HttpServer server;
	private Gson gson;

	private String sessionId;
	private long startTime;

	@Provides
	private GameDataServerConfig provideConfig(ConfigManager configManager) {
		return configManager.getConfig(GameDataServerConfig.class);
	}

	@Override
	protected void startUp() throws Exception {
		RuntimeTypeAdapterFactory<StratConfig> configAdapterFactory = RuntimeTypeAdapterFactory
			.of(StratConfig.class, "type") // Use "type" as the type field name
			.registerSubtype(MMConfig.class, "mmConfig");
		gson = new GsonBuilder()
			.registerTypeAdapterFactory(configAdapterFactory)
			.create();

		sessionId = UUID.randomUUID().toString().replace("-", "");
		startTime = Instant.now().getEpochSecond();

		server = HttpServer.create(new InetSocketAddress(SERVER_PORT), 0);
		server.createContext("/health", this::health);
		server.createContext("/snapshot", this::serveGameDataSnapshot);
		server.createContext("/session", this::serveSession);
		server.createContext("/exchange", this::serveExchangeData);
		server.createContext("/inventory", this::serveInventoryData);
		server.createContext("/player", this::servePlayerData);
		server.createContext("/config", this::serveLiveConfig);
		server.createContext("/chat", this::serveChatBox);
		server.setExecutor(Executors.newSingleThreadExecutor());
		server.start();
	}

	@Override
	protected void shutDown() throws Exception {
		server.stop(0);
	}

	private void sendResponse(HttpExchange httpExchange, Object data) throws IOException {
		httpExchange.sendResponseHeaders(200, 0);
		try (OutputStreamWriter out = new OutputStreamWriter(httpExchange.getResponseBody())) {
			gson.toJson(data, out);
		}
	}

	private void health(HttpExchange httpExchange) throws IOException {
		log.info("responding to health check");
		GameState state = client.getGameState();
		if (state != GameState.LOGGED_IN) {
			throw new GameDataServerException(
				String.format("Client is running, but got unexpected game state: %s", state)
			);
		}
		Map<String, String> response = Map.of("status", "healthy");
		sendResponse(httpExchange, response);
	}

	private void serveGameDataSnapshot(HttpExchange httpExchange) throws IOException {
		log.info("Fetching game data snapshot");
		GameDataSnapshot snapshot = GameDataSnapshot.builder()
			.session(getSession())
			.exchange(getExchangeData())
			.inventory(getInventoryData())
			.player(getPlayerData())
			.chatBox(getChatBox())
			.creationTime(Instant.now())
			.build();
		sendResponse(httpExchange, snapshot);
	}

	private void serveSession(HttpExchange httpExchange) throws IOException {
		log.info("Fetching session data");
		Session session = getSession();
		sendResponse(httpExchange, session);
	}

	private void serveExchangeData(HttpExchange httpExchange) throws IOException {
		log.info("Fetching exchange data");
		Exchange exchange = getExchangeData();
		sendResponse(httpExchange, exchange);
	}

	private void serveInventoryData(HttpExchange httpExchange) throws IOException {
		log.info("Fetching inventory data");
		Inventory inventory = getInventoryData();
		sendResponse(httpExchange, inventory);
	}

	private void servePlayerData(HttpExchange httpExchange) throws IOException {
		log.info("Fetching player data");
		Player player = getPlayerData();
		sendResponse(httpExchange, player);
	}

	private void serveLiveConfig(HttpExchange httpExchange) throws IOException {
		log.info("Fetching live config");
		TopLevelConfig topLevelConfig = TopLevelConfig.builder()
			.minGp(config.minGp())
			.build();

		List<StratConfig> stratConfigs = new ArrayList<>();
		stratConfigs.add(
			MMConfig.builder()
				.activated(config.mmActivated())
				.waitDuration(config.mmWaitDuration())
				.maxOfferTime(config.maxOfferTime())
				.build()
		);

		LiveConfig liveConfig = LiveConfig.builder()
			.autotraderOn(config.autotraderOn())
			.topLevelConfig(topLevelConfig)
			.stratConfigs(stratConfigs)
			.build();
		sendResponse(httpExchange, liveConfig);
	}

	private void serveChatBox(HttpExchange httpExchange) throws IOException {
		log.info("Fetching chat box contents");
		ChatBox chatBox = getChatBox();
		sendResponse(httpExchange, chatBox);
	}

	private Session getSession() {
		return Session.builder()
			.id(sessionId)
			.startTime(startTime)
			.playerName(client.getLocalPlayer().getName())
			.isF2p(client.getVarcIntValue(VarClientInt.MEMBERSHIP_STATUS) == 0)
			.build();
	}

	private Exchange getExchangeData() {
		GrandExchangeOffer[] offers = client.getGrandExchangeOffers();
		if (offers.length == 0) {
			throw new GameDataServerException("Unable to resolve exchange");
		}

		List<ExchangeSlot> slots = IntStream.range(0, Math.min(offers.length, MAX_GE_SLOTS))
			.mapToObj(i -> {
				GrandExchangeOffer offer = offers[i];
				if (offer.getState() == GrandExchangeOfferState.EMPTY) {
					return ExchangeSlot.asEmpty(i);
				}
				return ExchangeSlot.builder()
					.position(i)
					.itemId(offer.getItemId())
					.price(offer.getPrice())
					.quantityTransacted(offer.getQuantitySold())
					.totalQuantity(offer.getTotalQuantity())
					.state(ExchangeSlotState.fromGrandExchangeOfferState(offer.getState()))
					.build();
			})
			.collect(Collectors.toList());

		return Exchange.builder()
			.slots(slots)
			.build();
	}

	private Inventory getInventoryData() {
		ItemContainer itemContainer = client.getItemContainer(InventoryID.INVENTORY);
		if (itemContainer == null) {
			throw new GameDataServerException("Unable to resolve inventory");
		}

		List<Item> items = IntStream.range(0, MAX_INVENTORY_SLOTS)
			.mapToObj(i -> {
				net.runelite.api.Item slotItem = itemContainer.getItem(i);
				if (slotItem == null) {
					return null;
				}
				return Item.builder()
					.id(slotItem.getId())
					.quantity(slotItem.getQuantity())
					.inventoryPosition(i)
					.build();
			})
			.filter(Objects::nonNull)
			.collect(Collectors.toList());

		return Inventory.builder()
			.items(items)
			.build();
	}

	private Player getPlayerData() {
		boolean loggedIn = client.getGameState() == GameState.LOGGED_IN;

		Camera camera = Camera.builder()
			.z(client.getCameraZ())
			.yaw(client.getCameraYaw())
			.scale(client.getScale())
			.build();

		WorldPoint worldLocation = client.getLocalPlayer().getWorldLocation();
		Location location = Location.builder()
			.x(worldLocation.getX())
			.y(worldLocation.getY())
			.build();

		return Player.builder()
			.loggedIn(loggedIn)
			.location(location)
			.camera(camera)
			.build();
	}

	private String decodeUTF8(String input) {
		return input.replaceAll("[^\\x00-\\x7F]", " ");
	}

	private ChatBox getChatBox() {
		ChatLineBuffer buffer = client.getChatLineMap().get(ChatMessageType.PUBLICCHAT.getType());
		if (buffer == null) {
			return ChatBox.builder().build();
		}
		MessageNode[] lines = buffer.getLines();
		List<Message> messages = Arrays.stream(lines)
			.filter(Objects::nonNull)
			.map(l -> Message.builder()
				.content(decodeUTF8(l.getValue()))
				.sender(decodeUTF8(l.getName()))
				.timestamp(l.getTimestamp())
				.build())
			.collect(Collectors.toList());

		return ChatBox.builder()
			.messages(messages)
			.build();
	}
}
