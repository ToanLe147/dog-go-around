# 🏎️ Dog Go Around

> A fast-paced multiplayer racing game built with the Ursina engine

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Made with Ursina](https://img.shields.io/badge/made%20with-Ursina-orange.svg)](https://www.ursinaengine.org/)

---

## ✨ Features

- 🎮 **Multiplayer Racing** - Compete with friends in real-time
- 🌐 **Client-Server Architecture** - Authoritative server with snapshot interpolation
- 🏁 **Race System** - Checkpoints, laps, and finish line detection
- 🎯 **Physics Engine** - Realistic acceleration, steering, friction, and drift
- 📷 **Dynamic Camera** - Multiple camera modes with smooth following
- 🎨 **Interactive UI** - Lobby system, menus, and results screens
- ⚡ **Power-ups** - Boost mechanics for competitive gameplay
- 💬 **Chat System** - In-game communication

---

## 📦 Installation

### Prerequisites

- **Python 3.10+**
- **pip** package manager

### Setup

1. **Clone the repository**

   ```bash
   git clone https://github.com/yourusername/dog-go-around.git
   cd dog-go-around
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Required packages**

   ```
   ursina
   websockets
   msgpack
   numpy
   ```

---

## 🚀 Getting Started

### Starting the Server

```bash
python -m game.net.server --host 0.0.0.0 --port 7777
```

### Starting the Client

```bash
python run.py --server 127.0.0.1:7777 --name Player1
```

### Local Testing

1. Open a terminal and start the server
2. Open additional terminals for each client
3. Connect multiple clients to test multiplayer

---

## 📁 Project Structure

```
dog-go-around/
├── run.py                      # Main entry point
├── requirements.txt            # Python dependencies
└── game/
    ├── config.py              # Game configuration
    ├── core/                  # Core game logic
    │   ├── app.py            # Game application bootstrap
    │   ├── world.py          # World management
    │   ├── track.py          # Track system
    │   ├── car.py            # Player vehicle
    │   ├── camera_rig.py     # Camera controller
    │   ├── hud.py            # Heads-up display
    │   ├── physics.py        # Physics engine
    │   ├── race.py           # Race management
    │   ├── checkpoints.py    # Checkpoint system
    │   └── powerups.py       # Power-up system
    ├── ui/                    # User interface
    │   ├── menu.py           # Main menu
    │   ├── lobby.py          # Multiplayer lobby
    │   ├── pause_menu.py     # Pause screen
    │   └── results.py        # Race results
    ├── net/                   # Networking
    │   ├── server.py         # Game server
    │   ├── client.py         # Game client
    │   ├── messages.py       # Network messages
    │   └── state_sync.py     # State synchronization
    ├── assets/                # Game assets
    │   ├── textures/         # Texture files
    │   ├── models/           # 3D models
    │   └── sounds/           # Audio files
    ├── utils/                 # Utility modules
    │   ├── input_map.py      # Input handling
    │   ├── timing.py         # Time utilities
    │   ├── serialization.py  # Data serialization
    │   └── mathx.py          # Math helpers
    └── tests/                 # Unit tests
        ├── test_net.py       # Network tests
        └── test_physics.py   # Physics tests
```

---

## 🏗️ Architecture

### Core Classes

| Class | Description |
|-------|-------------|
| **GameApp** | Bootstraps Ursina engine, loads scenes, manages lifecycle |
| **RaceManager** | Controls race flow (countdown, laps, finish, results) |
| **Car** | Player vehicle entity with movement and collision |
| **Physics** | Handles acceleration, steering, friction, and drift |
| **Track** | Track mesh, boundaries, spawn points, lap management |
| **Checkpoints** | Waypoint validation and wrong-way detection |
| **HUD** | Display speedometer, lap counter, position, timer |
| **CameraRig** | Multiple camera modes with smooth following |
| **NetworkServer** | Authoritative game state and lobby management |
| **NetworkClient** | Input handling and state interpolation |
| **Messages** | Network message dataclasses |
| **UI Components** | Lobby, menu, and results interfaces |
| **InputMap** | Key binding configuration |

---

## 🎮 Controls

| Action | Keys |
|--------|------|
| **Throttle** | `W` / `↑` |
| **Brake/Reverse** | `S` / `↓` |
| **Steer Left** | `A` / `←` |
| **Steer Right** | `D` / `→` |
| **Handbrake** | `Space` |
| **Boost** | `Left Shift` |
| **Reset** | `R` |
| **Change Camera** | `C` |
| **Chat** | `T` |
| **Pause/Menu** | `Esc` |
| **Debug/FPS** | `F1` |

---

## 🎯 How to Play

1. **🌐 Connect** - Start the server and launch client with server address
2. **🎨 Lobby** - Select a track and ready up
3. **🏁 Race** - Pass checkpoints in order to complete laps
4. **⚡ Strategy** - Use boost on straights, handbrake for tight corners
5. **🏆 Win** - First player to complete all laps wins!

---

## 🌐 Networking

### Architecture

- **Client → Server**: Inputs sent at fixed rate
- **Server → Clients**: State snapshots broadcasted
- **Client-side**: Interpolation and prediction for smooth gameplay
- **Default Port**: 7777/UDP (WebSocket optional)

### Snapshot Contents

- Car transforms and velocities
- Race metadata (lap, position, time)
- Checkpoint states

---

## ⚙️ Configuration

### Config File

Edit `game/config.py` for:

- Resolution and FOV
- Physics constants
- Network tick rates
- Game rules

### Environment Variables

```bash
export DOG_SERVER_HOST=0.0.0.0
export DOG_SERVER_PORT=7777
export DOG_TICKRATE=60
export DOG_SNAPSHOT_RATE=30
```

---

## 🤝 Contributing

We welcome contributions! Here's how to help:

1. **Fork** the repository
2. **Create** a feature branch
3. **Write** tests for new features
4. **Run** linters and tests:

   ```bash
   pytest
   mypy .
   ruff check .
   ```

5. **Keep** assets under `assets/` with relative paths
6. **Prefer** small, testable modules

---

## 🐛 Troubleshooting

### Cannot Connect

- ✅ Verify host and port are correct
- ✅ Check firewall settings
- ✅ Ensure server and client versions match

### Rubber-banding / Lag

- ✅ Lower client graphics settings
- ✅ Adjust tick/snapshot rates in config
- ✅ Check network latency

### Physics Instability

- ✅ Cap FPS to 60
- ✅ Adjust `dt` clamp in Physics class
- ✅ Reduce physics substeps if needed

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

- Built with [Ursina Engine](https://www.ursinaengine.org/)
- Inspired by classic racing games

---

<div align="center">

**Made with ❤️ and Python**

[Report Bug](https://github.com/yourusername/dog-go-around/issues) · [Request Feature](https://github.com/yourusername/dog-go-around/issues)

</div>
