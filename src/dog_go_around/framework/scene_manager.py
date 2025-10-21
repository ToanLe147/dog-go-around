from __future__ import annotations
import pygame
from typing import Dict, Any, List, Type
from .scene import Scene


class SceneManager:
    """Manages scenes and shared state."""

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.shared: Dict[str, Any] = {}
        self._scenes: List[Scene] = []

    def push(self, scene: Scene):
        if self._scenes:
            self._scenes[-1].exit()
        self._scenes.append(scene)
        scene.enter()

    def replace(self, scene: Scene):
        if self._scenes:
            self._scenes[-1].exit()
            self._scenes.pop()
        self._scenes.append(scene)
        scene.enter()

    def pop(self):
        if self._scenes:
            self._scenes[-1].exit()
            self._scenes.pop()
        if self._scenes:
            self._scenes[-1].enter()

    @property
    def current(self) -> Scene | None:
        return self._scenes[-1] if self._scenes else None

    def handle_event(self, event: pygame.event.Event):
        if self.current:
            self.current.handle_event(event)

    def update(self, dt: float):
        if self.current:
            self.current.update(dt)

    def draw(self):
        if self.current:
            self.current.draw()
