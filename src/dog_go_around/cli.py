"""Entry point launching the Pygame-based framework demo."""

from __future__ import annotations
import sys
import argparse
import asyncio
import pygame
from dog_go_around.framework import config
from dog_go_around.framework.display_manager import DisplayManager
from dog_go_around.framework.scene_manager import SceneManager
from dog_go_around.framework.sound_manager import SoundManager
from dog_go_around.scenes.main_menu import MainMenuScene
from dog_go_around.scenes.demo import DemoScene


async def async_main(fullscreen=False):
    """Async game loop for pygbag/web support."""
    print("[DEBUG] Starting async_main...")
    pygame.init()
    print("[DEBUG] pygame.init() completed")
    clock = pygame.time.Clock()

    display = DisplayManager()
    if fullscreen:
        display.fullscreen = True
    screen = display.apply()
    print("[DEBUG] Display applied - screen created")

    manager = SceneManager(screen)
    shared = manager.shared

    # Initialize sound manager and add a 'click' tone
    sound = SoundManager()
    sound.init()
    print("[DEBUG] SoundManager initialized")
    sound.generate_tone("click", frequency_hz=880.0, duration_ms=70, volume=0.5)
    print("[DEBUG] Click tone generated (or skipped if numpy unavailable)")
    shared["sound"] = sound

    def start_game():
        manager.replace(DemoScene(screen, to_menu, shared=shared))

    def toggle_fullscreen():
        nonlocal screen
        screen = display.toggle_fullscreen(screen)
        # Scenes need updated screen surface reference
        manager.screen = screen

    def to_menu():
        manager.replace(
            MainMenuScene(screen, start_game, toggle_fullscreen, shared=shared)
        )

    # Start with menu
    manager.push(MainMenuScene(screen, start_game, toggle_fullscreen, shared=shared))
    print("[DEBUG] MainMenuScene pushed to scene manager")

    running = True
    frame_count = 0
    while running:
        dt = clock.tick(config.FPS) / 1000.0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False
            else:
                manager.handle_event(event)

        manager.update(dt)
        manager.draw()
        pygame.display.flip()

        # Log first frame to confirm rendering started
        if frame_count == 0:
            print("[DEBUG] First frame drawn")
        frame_count += 1

        # Yield control to browser on web platform
        await asyncio.sleep(0)

    pygame.quit()


def main():
    """Entry point for desktop/CLI execution."""
    parser = argparse.ArgumentParser(
        description="Dog Go Around - Pygame Framework Demo"
    )
    parser.add_argument("--fullscreen", action="store_true", help="Start in fullscreen")
    args = parser.parse_args()

    # Run async main loop
    asyncio.run(async_main(fullscreen=args.fullscreen))


if __name__ == "__main__":
    main()
