from __future__ import annotations
import pygame
from typing import Tuple, Dict, Any, Optional


class Scene:
    """Base class for all scenes.

    Subclasses should override handle_event, update, and draw.
    """

    def __init__(self, screen: pygame.Surface, shared: Optional[Dict[str, Any]] = None):
        self.screen = screen
        self.shared = shared if shared is not None else {}
        self.is_active = False

    # Lifecycle hooks
    def enter(self):
        self.is_active = True

    def exit(self):
        self.is_active = False

    # Frame hooks
    def handle_event(self, event: pygame.event.Event):
        pass

    def update(self, dt: float):
        pass

    def draw(self):
        pass
