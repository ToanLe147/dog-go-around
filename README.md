# Dog Go Around — Pygame Framework

This repository contains a small, reusable Pygame framework for 2D games. It runs locally and can be published to the web using WebAssembly via pygbag.

What’s included:

- Components: Button, Health Bar, Title, Slider
- Sound Manager: play sounds based on events from components/scenes
- Scene: container for visualization and logic
- Scene Manager: manages scene switching and a shared state dict
- Display Manager: toggles fullscreen and resolution from triggers
- Assets folder: central place for images/audio (path exposed via `config`)

Defaults (configurable):

- Initial window size: 640 × 360
- Game name/title/icon
- Assets directory path via `src/framework/config.py`

## Project layout

```text
assets/                    # put your images/audio here
main.py                    # pygbag entry point (web deployment)
index.html                 # web page template for pygbag
pygbag.json                # pygbag configuration
src/
  dog_go_around/
    __init__.py            # package root with version
    __main__.py            # enables python -m dog_go_around
    cli.py                 # main entry point (async-compatible)
    framework/
      components/
        button.py
        health_bar.py
        slider.py
        title.py
      config.py            # paths, window defaults, colors
      display_manager.py   # resolution/fullscreen toggles
      scene.py             # base Scene class
      scene_manager.py     # manages current scene
      sound_manager.py     # sound playback by key
    scenes/
      main_menu.py         # demo main menu scene
      demo.py              # demo scene showcasing components
tests/
  test_sound_manager.py    # example pytest
```

## Quick start

Install dependencies (Python 3.10+):

```bash
pip install -r requirements.txt
```

Run the demo:

```bash
uv run dog-go-around
# or
python -m dog_go_around
```

Optional flags:

```bash
uv run dog-go-around --fullscreen
```

You can also use the packaged console script if installed via `pip`:

```bash
# After pip install -e .
dog-go-around
```

## Using the framework

- Create your own scenes under `src/dog_go_around/scenes/` by subclassing `Scene`.
- Add UI components from `dog_go_around.framework.components` to your scenes.
- Use `DisplayManager` to change resolution/fullscreen in response to events.
- Load sounds via `SoundManager` (place files under `assets/`).

Access the assets path and default settings via:

```python
from dog_go_around.framework import config
print(config.ASSETS_DIR)
print(config.INITIAL_WINDOW_SIZE)
```

## Web deployment (pygbag)

This framework is fully compatible with pygbag for running in the browser!

**📖 See [PYGBAG_DEPLOYMENT.md](PYGBAG_DEPLOYMENT.md) for complete deployment guide**

### Quick build

```bash
# Install pygbag if needed
pip install pygbag

# Build the web version (creates build/web directory)
pygbag .
```

The build creates a `build/web/` directory with all files needed for deployment.

### Test locally

```bash
# Run local web server (opens browser automatically)
pygbag --build .

# Or serve manually
python -m http.server -d build/web 8000
# Then visit http://localhost:8000
```

### Deploy to GitHub Pages

1. Build the web version: `pygbag .`
2. Copy `build/web/*` to your gh-pages branch or docs folder
3. Enable GitHub Pages in repository settings
4. Your game will be live at `https://username.github.io/repo-name`

### How it works

- `main.py` at project root is the pygbag entry point
- The game loop uses `asyncio` to yield control to the browser
- `index.html` customizes the web page appearance
- Asset loading works the same as desktop (via `config.ASSETS_DIR`)

### Web limitations

- Some pygame features may not be available (check pygbag docs)
- File I/O is limited (use IndexedDB for persistence if needed)
- Audio may require user interaction to start
- Performance varies by browser

## License

MIT (see LICENSE if present) — assets you add may have their own licenses.
