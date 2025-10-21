from __future__ import annotations
import pygame
from ..framework.scene import Scene
from ..framework.components.health_bar import HealthBar
from ..framework.components.slider import Slider
from ..framework.components.button import Button
from ..framework import config


class DemoScene(Scene):
    def __init__(self, screen: pygame.Surface, to_menu, shared=None):
        super().__init__(screen, shared)
        w, h = self.screen.get_size()
        self.health = HealthBar(pygame.Rect(20, 20, 200, 18))
        self.slider = Slider(pygame.Rect(20, 60, 240, 16))

        def wrap(cb):
            def _inner():
                snd = (
                    self.shared.get("sound") if isinstance(self.shared, dict) else None
                )
                if snd:
                    snd.play("click")
                cb()

            return _inner

        self.back_btn = Button("Back", pygame.Rect(20, h - 50, 100, 32), wrap(to_menu))

    def handle_event(self, event: pygame.event.Event):
        self.slider.handle_event(event)
        self.back_btn.handle_event(event)

    def update(self, dt: float):
        # Sync health with slider for demo
        self.health.set(int(100 * self.slider.value))

    def draw(self):
        self.screen.fill((30, 30, 30))
        self.health.draw(self.screen)
        self.slider.draw(self.screen)
        self.back_btn.draw(self.screen)
