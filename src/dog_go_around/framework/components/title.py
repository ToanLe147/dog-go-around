from __future__ import annotations
import pygame
from .. import config


class Title:
    def __init__(self, text: str, center: tuple[int, int], color=(255, 255, 200)):
        self.text = text
        self.center = center
        self.font = pygame.font.Font(config.FONT_NAME, 42)
        self.color = color

    def draw(self, surface: pygame.Surface):
        label = self.font.render(self.text, True, self.color)
        rect = label.get_rect(center=self.center)
        surface.blit(label, rect)
