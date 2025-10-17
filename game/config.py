"""Game configuration settings."""

import os

# Display settings
WINDOW_TITLE = "Dog Go Around - Racing Game"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
FULLSCREEN = os.environ.get("FULLSCREEN", "0") == "1"

# Game settings
MAX_SPEED = 300  # pixels per second
ACCELERATION = 150
FRICTION = 0.95
TURN_SPEED = 200  # degrees per second
DRIFT_FACTOR = 0.92

# Track settings
TRACK_WIDTH = 100
CHECKPOINT_SIZE = 80

# Physics
COLLISION_SLOWDOWN = 0.5

# Network settings
DEFAULT_SERVER_HOST = "127.0.0.1"
DEFAULT_SERVER_PORT = 7777
NETWORK_UPDATE_RATE = 30  # updates per second

# Audio settings
MUSIC_VOLUME = 0.7
SFX_VOLUME = 0.8

# Colors (RGB)
COLOR_BACKGROUND = (34, 139, 34)  # Forest green
COLOR_TRACK = (64, 64, 64)  # Dark gray
COLOR_TRACK_BORDER = (255, 255, 255)  # White
COLOR_PLAYER = (0, 0, 255)  # Blue
COLOR_OPPONENT = (255, 0, 0)  # Red
COLOR_CHECKPOINT = (255, 255, 0)  # Yellow
COLOR_TEXT = (255, 255, 255)  # White
COLOR_UI_BG = (0, 0, 0, 180)  # Semi-transparent black
