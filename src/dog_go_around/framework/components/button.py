from __future__ import annotations
import pygame
from typing import Callable, Tuple
from .. import config


class Button:
    def __init__(
        self,
        text: str,
        rect: pygame.Rect,
        on_click: Callable[[], None],
        font: pygame.font.Font | None = None,
        bg=(60, 60, 60),
        fg=(255, 255, 255),
        hover_bg=(90, 90, 90),
    ):
        self.text = text
        self.rect = pygame.Rect(rect)
        self.on_click = on_click
        self.font = font or pygame.font.Font(config.FONT_NAME, 20)
        self.bg = bg
        self.hover_bg = hover_bg
        self.fg = fg
        self._hover = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEMOTION:
            self._hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(
            surface,
            self.hover_bg if self._hover else self.bg,
            self.rect,
            border_radius=6,
        )
        label = self.font.render(self.text, True, self.fg)
        surface.blit(label, label.get_rect(center=self.rect.center))
