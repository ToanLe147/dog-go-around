from __future__ import annotations
import os
from typing import Dict
import numpy as np
import pygame
from . import config


class SoundManager:
    """Plays sounds by string key based on events from components."""

    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self._ready = False

    def init(self):
        """Initialize mixer; try dummy driver if normal audio fails."""
        if pygame.mixer.get_init():
            self._ready = True
            return
        try:
            pygame.mixer.init()
            self._ready = True
            return
        except Exception:
            pass
        # Fallback to dummy audio driver
        try:
            if os.environ.get("SDL_AUDIODRIVER") is None:
                os.environ["SDL_AUDIODRIVER"] = "dummy"
            pygame.mixer.init()
            self._ready = True
        except Exception:
            self._ready = False

    def load(self, key: str, filename: str):
        if not self._ready:
            self.init()
        if not self._ready:
            return
        try:
            path = config.ASSETS_DIR / filename
            self.sounds[key] = pygame.mixer.Sound(str(path))
        except Exception:
            pass

    def generate_tone(
        self,
        key: str,
        frequency_hz: float = 880.0,
        duration_ms: int = 60,
        volume: float = 0.4,
    ):
        """Generate a short beep tone and store it under the given key.

        Uses numpy to synthesize a sine wave compatible with pygame.sndarray.
        """
        if not self._ready:
            self.init()
        if not self._ready:
            return
        try:
            sample_rate = 44100
            n_samples = int(sample_rate * (duration_ms / 1000.0))
            t = np.linspace(0, duration_ms / 1000.0, n_samples, False)
            wave = 0.5 * np.sin(2 * np.pi * frequency_hz * t)
            # 16-bit signed mono
            audio = (wave * 32767).astype(np.int16)
            snd = pygame.mixer.Sound(buffer=audio.tobytes())
            snd.set_volume(max(0.0, min(1.0, volume)))
            self.sounds[key] = snd
        except Exception:
            pass

    def play(self, key: str):
        if self._ready and key in self.sounds:
            try:
                self.sounds[key].play()
            except Exception:
                pass
