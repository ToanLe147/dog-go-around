"""Framework configuration and paths."""

from __future__ import annotations
import os
from pathlib import Path

# Project root is the directory containing this file's grandparent
PROJECT_ROOT = Path(__file__).resolve().parents[2]
ASSETS_DIR = PROJECT_ROOT / "assets"

# Display
GAME_NAME = "Dog Go Around"
WINDOW_TITLE = "Dog Go Around"
WINDOW_ICON = None  # path to icon in assets if available
INITIAL_WINDOW_SIZE = (640, 360)
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (60, 60, 60)
DARK_BLUE = (24, 32, 48)
BLUE = (28, 120, 240)
GREEN = (0, 200, 0)
RED = (220, 40, 40)

# Misc
FONT_NAME = None  # use default pygame font if None
