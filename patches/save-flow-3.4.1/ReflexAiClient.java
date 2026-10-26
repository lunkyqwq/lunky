package com.example.reflexai.client;

import com.example.reflexai.ReflexAiMod;
import net.fabricmc.api.ClientModInitializer;
import net.fabricmc.fabric.api.client.event.lifecycle.v1.ClientTickEvents;
import net.fabricmc.fabric.api.client.rendering.v1.EntityRendererRegistry;
import net.fabricmc.fabric.api.client.screen.v1.ScreenEvents;
import net.fabricmc.loader.api.FabricLoader;
import net.minecraft.client.MinecraftClient;
import net.minecraft.client.gui.screen.Screen;
import net.minecraft.client.gui.screen.TitleScreen;
import net.minecraft.client.gui.screen.world.CreateWorldScreen;
import net.minecraft.client.gui.widget.ButtonWidget;
import net.minecraft.client.render.entity.ZombieEntityRenderer;
import net.minecraft.client.render.entity.EntityRendererFactory;
import net.minecraft.client.render.entity.EntityRenderer;
import net.minecraft.text.Text;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;

/** Client setup, including a safe first-launch prompt for a separate training save. */
public final class ReflexAiClient implements ClientModInitializer {
    private static final Logger LOGGER = LoggerFactory.getLogger("reflexai/client");
    private static final String TRAINING_WORLD_NAME = "Reflex AI Training";
    private static final Path FIRST_LAUNCH_MARKER = FabricLoader.getInstance()
        .getConfigDir().resolve("reflexai").resolve("training-world-prompted");
    private static boolean firstLaunchCheckDone;
    private static boolean prefillNextCreateWorld;
    private static boolean pendingTrainingWorldStart;

    @Override
    @SuppressWarnings({"rawtypes", "unchecked"})
    public void onInitializeClient() {
        EntityRendererRegistry.register(ReflexAiMod.TRAINER_TYPE,
            (EntityRendererFactory) (EntityRendererFactory.Context context) -> (EntityRenderer) new ZombieEntityRenderer(context));

        ScreenEvents.AFTER_INIT.register((client, screen, scaledWidth, scaledHeight) -> {
            if (screen instanceof TitleScreen) {
                addTrainingWorldButton(client, screen, scaledWidth, scaledHeight);
            }
            if (screen instanceof CreateWorldScreen createWorldScreen && prefillNextCreateWorld) {
                prefillNextCreateWorld = false;
                createWorldScreen.getWorldCreator().setWorldName(TRAINING_WORLD_NAME);
                createWorldScreen.getWorldCreator().setCheatsEnabled(true);
                createWorldScreen.getWorldCreator().update();
            }
        });

        ClientTickEvents.END_CLIENT_TICK.register(ReflexAiClient::checkFirstLaunch);
    }

    private static void addTrainingWorldButton(MinecraftClient client, Screen screen, int width, int height) {
        screen.addDrawableChild(ButtonWidget.builder(Text.literal("Reflex AI 训练存档"), button -> openTrainingWorldCreator(client))
            .dimensions(width / 2 - 100, height - 42, 200, 20)
            .build());
    }

    private static void checkFirstLaunch(MinecraftClient client) {
        if (pendingTrainingWorldStart && client.world != null) {
            pendingTrainingWorldStart = false;
            markFirstLaunchPrompted();
        } else if (pendingTrainingWorldStart && client.currentScreen instanceof TitleScreen) {
            // The player returned from Create World without entering the new world.
            // Leave the marker absent so the prompt can be shown again next launch.
            pendingTrainingWorldStart = false;
        }

        if (firstLaunchCheckDone || !(client.currentScreen instanceof TitleScreen)) return;
        firstLaunchCheckDone = true;
        if (Files.exists(FIRST_LAUNCH_MARKER)) return;

        client.execute(() -> openTrainingWorldCreator(client));
    }

    private static void markFirstLaunchPrompted() {
        try {
            Files.createDirectories(FIRST_LAUNCH_MARKER.getParent());
            Files.writeString(FIRST_LAUNCH_MARKER,
                "The Reflex AI training-world creation screen was opened once.\n");
        } catch (IOException exception) {
            LOGGER.warn("Could not write Reflex AI first-launch marker; the prompt may appear again.", exception);
        }
    }

    private static void openTrainingWorldCreator(MinecraftClient client) {
        prefillNextCreateWorld = true;
        pendingTrainingWorldStart = true;
        CreateWorldScreen.show(client, () -> {});
    }
}
