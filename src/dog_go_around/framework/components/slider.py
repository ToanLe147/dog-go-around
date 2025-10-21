from __future__ import annotations
import pygame


class Slider:
    def __init__(
        self,
        rect: pygame.Rect,
        min_value: float = 0.0,
        max_value: float = 1.0,
        value: float = 0.5,
        bg=(60, 60, 60),
        bar=(120, 120, 120),
        knob=(240, 240, 240),
    ):
        self.rect = pygame.Rect(rect)
        self.min = min_value
        self.max = max_value
        self.value = value
        self.bg = bg
        self.bar = bar
        self.knob = knob
        self.dragging = False

    def handle_event(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.dragging = True
                self._set_value_from_pos(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.dragging = False
        elif event.type == pygame.MOUSEMOTION and self.dragging:
            self._set_value_from_pos(event.pos[0])

    def _set_value_from_pos(self, x: int):
        t = (x - self.rect.left) / max(1, self.rect.width)
        t = max(0.0, min(1.0, t))
        self.value = self.min + t * (self.max - self.min)

    def draw(self, surface: pygame.Surface):
        # Track
        pygame.draw.rect(surface, self.bg, self.rect, border_radius=4)
        # Fill proportion
        fill_w = int(
            self.rect.width
            * ((self.value - self.min) / max(1e-6, (self.max - self.min)))
        )
        fill_rect = pygame.Rect(self.rect.left, self.rect.top, fill_w, self.rect.height)
        pygame.draw.rect(surface, self.bar, fill_rect, border_radius=4)
        # Knob
        knob_x = self.rect.left + fill_w
        knob_rect = pygame.Rect(knob_x - 6, self.rect.centery - 10, 12, 20)
        pygame.draw.rect(surface, self.knob, knob_rect, border_radius=4)
