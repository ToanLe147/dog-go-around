"""Entry point launching the Pygame-based framework demo."""

from __future__ import annotations
import argparse
import pygame
from dog_go_around.framework import config
from dog_go_around.framework.display_manager import DisplayManager
from dog_go_around.framework.scene_manager import SceneManager
from dog_go_around.framework.sound_manager import SoundManager
from dog_go_around.scenes.main_menu import MainMenuScene
from dog_go_around.scenes.demo import DemoScene


def main():
    parser = argparse.ArgumentParser(
        description="Dog Go Around - Pygame Framework Demo"
    )
    parser.add_argument("--fullscreen", action="store_true", help="Start in fullscreen")
    args = parser.parse_args()

    pygame.init()
    clock = pygame.time.Clock()

    display = DisplayManager()
    if args.fullscreen:
        display.fullscreen = True
    screen = display.apply()

    manager = SceneManager(screen)
    shared = manager.shared

    # Initialize sound manager and add a 'click' tone
    sound = SoundManager()
    sound.init()
    sound.generate_tone("click", frequency_hz=880.0, duration_ms=70, volume=0.5)
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

    running = True
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

    pygame.quit()


if __name__ == "__main__":
    main()
