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
src/
  dog_go_around/
    __init__.py            # package root with version
    __main__.py            # enables python -m dog_go_around
    cli.py                 # main entry point
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

## Web (pygbag)

This codebase is compatible with pygbag (listed in `requirements.txt`). Publishing to the web typically involves preparing a minimal entry file and running pygbag; consult pygbag docs for packaging steps.

## License

MIT (see LICENSE if present) — assets you add may have their own licenses.
