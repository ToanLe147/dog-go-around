import os
import pytest
import pygame

from dog_go_around.framework.sound_manager import SoundManager


def _init_mixer_dummy_if_needed():
    try:
        if not pygame.mixer.get_init():
            # prefer dummy driver for CI/non-audio envs
            if os.environ.get("SDL_AUDIODRIVER") is None:
                os.environ["SDL_AUDIODRIVER"] = "dummy"
            pygame.mixer.init()
        return True
    except Exception:
        return False


def test_generate_tone_and_play():
    if not _init_mixer_dummy_if_needed():
        pytest.skip("Audio mixer unavailable; skipping sound test")

    sm = SoundManager()
    sm.init()
    assert sm._ready, "SoundManager failed to initialize"

    # Generate a short click tone and ensure play doesn't raise
    sm.generate_tone("click", frequency_hz=880.0, duration_ms=30, volume=0.2)
    sm.play("click")

    # If we reached here without exceptions, treat as success
    assert "click" in sm.sounds
