from __future__ import annotations
import pygame
from typing import Callable
from ..framework.scene import Scene
from ..framework.components.button import Button
from ..framework.components.title import Title
from ..framework import config


class MainMenuScene(Scene):
    def __init__(
        self,
        screen: pygame.Surface,
        start_game: Callable[[], None],
        toggle_fullscreen: Callable[[], None],
        shared=None,
    ):
        super().__init__(screen, shared)
        w, h = self.screen.get_size()
        self.title = Title("Dog Go Around", (w // 2, h // 2 - 80))

        def wrap(cb: Callable[[], None]):
            def _inner():
                snd = (
                    self.shared.get("sound") if isinstance(self.shared, dict) else None
                )
                if snd:
                    snd.play("click")
                cb()

            return _inner

        self.buttons: list[Button] = [
            Button(
                "Start",
                pygame.Rect(w // 2 - 80, h // 2 - 10, 160, 36),
                wrap(start_game),
            ),
            Button(
                "Toggle Fullscreen",
                pygame.Rect(w // 2 - 120, h // 2 + 40, 240, 36),
                wrap(toggle_fullscreen),
            ),
            Button(
                "Quit",
                pygame.Rect(w // 2 - 80, h // 2 + 90, 160, 36),
                wrap(lambda: setattr(self, "_quit", True)),
            ),
        ]
        self._quit = False

    def handle_event(self, event: pygame.event.Event):
        for b in self.buttons:
            b.handle_event(event)

    def update(self, dt: float):
        pass

    def draw(self):
        self.screen.fill(config.DARK_BLUE)
        self.title.draw(self.screen)
        for b in self.buttons:
            b.draw(self.screen)

    def should_quit(self) -> bool:
        return self._quit
