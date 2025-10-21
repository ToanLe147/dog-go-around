from __future__ import annotations
import pygame


class HealthBar:
    def __init__(
        self,
        rect: pygame.Rect,
        max_value: int = 100,
        value: int = 100,
        bg=(40, 40, 40),
        fg=(220, 60, 60),
    ):
        self.rect = pygame.Rect(rect)
        self.max = max_value
        self.value = value
        self.bg = bg
        self.fg = fg

    def set(self, value: int):
        self.value = max(0, min(self.max, value))

    def add(self, delta: int):
        self.set(self.value + delta)

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.bg, self.rect, border_radius=4)
        if self.max > 0:
            w = int(self.rect.width * (self.value / self.max))
            bar_rect = pygame.Rect(self.rect.left, self.rect.top, w, self.rect.height)
            pygame.draw.rect(surface, self.fg, bar_rect, border_radius=4)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, width=1, border_radius=4)
