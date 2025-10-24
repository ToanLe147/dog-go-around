# Pygbag Web Deployment Guide

This guide explains how to deploy your Dog Go Around game to the web using pygbag.

## Prerequisites

```bash
pip install pygbag
```

## Quick Start

### 1. Build for web

From your project root:

```bash
pygbag .
```

This creates a `build/web/` directory with:

- Your game compiled to WebAssembly
- index.html (customized from your template)
- All necessary JavaScript/Python runtime files
- Assets from your `assets/` folder

### 2. Test locally

```bash
# Option 1: pygbag's built-in server (recommended)
pygbag --build .
# Opens browser automatically at http://localhost:8000

# Option 2: Manual server
python -m http.server -d build/web 8000
# Visit http://localhost:8000 in your browser
```

### 3. Deploy to hosting

#### GitHub Pages (recommended)

```bash
# 1. Build
pygbag .

# 2. Create/switch to gh-pages branch
git checkout -b gh-pages

# 3. Copy build files
cp -r build/web/* .
git add .
git commit -m "Deploy game to GitHub Pages"
git push origin gh-pages

# 4. Enable in GitHub repo settings → Pages → Source: gh-pages branch
```

Your game will be live at: `https://username.github.io/repository-name`

#### Itch.io

```bash
# 1. Build
pygbag .

# 2. Zip the web folder
cd build
zip -r game.zip web/

# 3. Upload to itch.io
# - Create new project
# - Set "Kind of project" to HTML
# - Upload game.zip
# - Check "This file will be played in the browser"
```

#### Netlify/Vercel

```bash
# 1. Build
pygbag .

# 2. Deploy build/web directory
# Netlify: drag build/web folder to netlify.com/drop
# Vercel: vercel build/web
```

## Customization

### index.html

Edit `index.html` in your project root to customize:

- Page title and header
- Styling (colors, fonts, layout)
- Loading screen
- Canvas size
- Footer links

### pygbag.json

Configure build settings in `pygbag.json`:

```json
{
  "package": "dog_go_around",
  "title": "Your Game Title",
  "width": 640,
  "height": 360,
  "template": "index.html"
}
```

## Troubleshooting

### Game doesn't load

- Check browser console (F12) for errors
- Ensure all assets are in the `assets/` folder
- Verify `main.py` is at project root
- Check that async/await is used in game loop

### Audio doesn't work

- Web audio requires user interaction
- Add a "Click to start" screen if needed
- Use `SoundManager.init()` after user input

### Performance issues

- Optimize asset sizes (compress images/audio)
- Reduce FPS if needed (edit `config.FPS`)
- Profile with browser dev tools

### Assets not found

- Ensure paths use `config.ASSETS_DIR`
- Don't use absolute paths
- Assets must be in `assets/` folder before build

## How it works

### Async game loop

The game loop uses `asyncio.sleep(0)` to yield control:

```python
while running:
    # ... game logic ...
    await asyncio.sleep(0)  # Yield to browser
```

This prevents blocking the browser's event loop.

### Entry points

- **Desktop**: `src/dog_go_around/cli.py` → `asyncio.run(async_main())`
- **Web**: `main.py` → imported by pygbag, runs in browser

### Asset loading

Works the same as desktop:

```python
from dog_go_around.framework import config
icon_path = config.ASSETS_DIR / "icon.png"
```

## Best practices

1. **Test locally** before deploying
2. **Keep assets small** - web bandwidth matters
3. **Provide loading feedback** - customize index.html
4. **Handle audio carefully** - require user interaction
5. **Version your builds** - tag releases in git

## Resources

- [Pygbag documentation](https://pygame-web.github.io/)
- [Pygame web limitations](https://pygame-web.github.io/wiki/pygbag/)
- [Example games](https://github.com/pygame-web/pygbag#showcase)
