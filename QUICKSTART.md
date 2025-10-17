# Quick Start Guide

## Installation

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Verify installation:**

   ```bash
   python -c "import ursina; print('Ursina installed successfully')"
   ```

## Running the Game

### Single Player (Offline Mode)

Run the game in offline mode without multiplayer:

```bash
python run.py --offline
```

or

```bash
uv run run.py --offline
```

### Multiplayer

#### Start the Server

In one terminal, start the game server:

```bash
python -m game.net.server --host 0.0.0.0 --port 7777
```

#### Start the Client

In another terminal (or on another computer), connect to the server:

```bash
python run.py --server 127.0.0.1:7777 --name Player1
```

For additional players, open more terminals:

```bash
python run.py --server 127.0.0.1:7777 --name Player2
python run.py --server 127.0.0.1:7777 --name Player3
```

## Controls

| Action | Keys |
|--------|------|
| **Throttle** | W or ↑ |
| **Brake/Reverse** | S or ↓ |
| **Steer Left** | A or ← |
| **Steer Right** | D or → |
| **Handbrake** | Space |
| **Boost** | Left Shift |
| **Reset Car** | R |
| **Change Camera** | C |
| **Pause** | Esc |

## Game Features

### Main Menu

- Start Race: Begin a new race
- Options: (Coming soon)
- Quit: Exit the game

### Racing

- Complete checkpoints in order
- Finish the required number of laps
- First to complete all laps wins!

### HUD Information

- **Speed**: Current speed in km/h
- **Lap Counter**: Current lap / Total laps
- **Position**: Your race position
- **Timer**: Current race time

## Troubleshooting

### Game won't start

- Make sure all dependencies are installed
- Check Python version (3.10+ required)

### Controls not working

- Make sure the game window has focus
- Try clicking in the game window

### Network connection issues

- Verify server is running first
- Check firewall settings
- Ensure correct host/port

### Performance issues

- Lower screen resolution in config.py
- Disable shadows: `ENABLE_SHADOWS = False`
- Disable antialiasing: `ENABLE_ANTIALIASING = False`

## Configuration

Edit `game/config.py` to customize:

```python
# Display
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
FPS_CAP = 60

# Physics
MAX_SPEED = 50.0
ACCELERATION = 15.0
TURN_SPEED = 120.0

# Race
LAP_COUNT = 3
```

## Adding Assets

Place your own assets in the `game/assets/` directory:

- **Textures**: `.png` or `.jpg` files in `game/assets/textures/`
- **Models**: `.obj` or `.fbx` files in `game/assets/models/`
- **Sounds**: `.wav` or `.ogg` files in `game/assets/sounds/`

Remove the `.txt` placeholder files after adding real assets.

## Running Tests

Run the test suite:

```bash
pytest game/tests/ -v
```

Run specific test file:

```bash
pytest game/tests/test_physics.py -v
```

## Development

### Project Structure

```
dog-go-around/
├── run.py              # Main entry point
├── game/
│   ├── config.py       # Configuration
│   ├── core/           # Core game logic
│   ├── ui/             # User interface
│   ├── net/            # Networking
│   ├── utils/          # Utilities
│   └── assets/         # Game assets
└── tests/              # Unit tests
```

### Adding New Features

1. Core gameplay: Add to `game/core/`
2. UI screens: Add to `game/ui/`
3. Network features: Add to `game/net/`
4. Utilities: Add to `game/utils/`

## Next Steps

- Replace placeholder assets with real textures, models, and sounds
- Customize physics values in `config.py`
- Add more tracks in `game/core/track.py`
- Implement additional power-ups
- Create custom car models

Enjoy racing! 🏎️💨
