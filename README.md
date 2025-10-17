# Dog Go Around — Pyglet Edition

A simple top‑down racing prototype built with Pyglet. It features smooth car controls, an oval track with checkpoints, a basic menu, and a lightweight HUD.

## Features

- Top‑down racing with velocity/angle based car physics
- WASD/Arrow controls and a keyboard/mouse‑driven main menu
- Oval track with inner/outer borders, dashed center line, and checkpoint markers
- HUD showing speed, lap placeholder, and control hints
- Pause overlay (ESC) with resume and quit‑to‑menu
- 60 FPS target

## Quick start

Install dependencies and run the game.

```bash
# Using uv (recommended)
uv sync
uv run run.py --offline

# Or using pip
pip install -r requirements.txt
python run.py --offline
```

## Controls

- Menu: Up/Down or Mouse to navigate, Enter/Space/Click to select
- Race: W/Up accelerate, S/Down brake, A/Left and D/Right steer, ESC pause
- Pause: ESC resume, Q back to menu

## Project structure

```text
dog-go-around/
├── game/
│   ├── config.py          # Settings for window, physics, colors
│   ├── game.py            # Main loop and state machine
│   ├── core/
│   │   ├── car.py         # Car physics and rendering
│   │   └── track.py       # Track geometry and rendering
│   └── ui/
│       ├── hud.py         # HUD overlay
│       └── menu.py        # Main menu
├── run.py                 # CLI entry point
├── pyproject.toml         # Project metadata and dependencies
└── README.md
```

## Configuration

Tweak `game/config.py` values.

```python
# Display
WINDOW_TITLE = "Dog Go Around - Racing Game"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
FPS = 60
FULLSCREEN = False

# Physics
MAX_SPEED = 300
ACCELERATION = 150
FRICTION = 0.95
TURN_SPEED = 200

# Track
TRACK_WIDTH = 100
CHECKPOINT_SIZE = 80

# Colors (RGB)
COLOR_BACKGROUND = (34, 139, 34)
COLOR_TRACK = (64, 64, 64)
COLOR_PLAYER = (0, 0, 255)
COLOR_TEXT = (255, 255, 255)
```

## Tips and customization

- Add an opponent: create another `Car` in `game/game.py` and append it to `self.cars`.
- Change track size: adjust `radius_x`/`radius_y` in `game/core/track.py`.
- Tune handling: edit physics values in `game/config.py`.

## Limitations

- Single local player
- No AI yet
- Networking not implemented
- Single track

## License

MIT
