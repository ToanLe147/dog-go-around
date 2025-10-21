from __future__ import annotations
import pygame
from typing import Tuple
from . import config


class DisplayManager:
    """Manages display settings via events.

    Provides APIs to toggle fullscreen and change resolution
    based on triggers from components/scenes.
    """

    def __init__(self):
        self.fullscreen = False
        self.size = config.INITIAL_WINDOW_SIZE

    def apply(self) -> pygame.Surface:
        flags = pygame.FULLSCREEN if self.fullscreen else 0
        screen = pygame.display.set_mode(self.size, flags)
        pygame.display.set_caption(config.WINDOW_TITLE)
        # Optional icon
        # if config.WINDOW_ICON:
        #     try:
        #         icon = pygame.image.load(str(config.ASSETS_DIR / config.WINDOW_ICON)).convert_alpha()
        #         pygame.display.set_icon(icon)
        #     except Exception:
        #         pass
        return screen

    def toggle_fullscreen(self, screen: pygame.Surface) -> pygame.Surface:
        self.fullscreen = not self.fullscreen
        return self.apply()

    def set_resolution(self, size: Tuple[int, int]) -> pygame.Surface:
        self.size = size
        return self.apply()
