"""Assets documentation.

This directory contains game assets:

## Textures (game/assets/textures/)

- grass.png/jpg - Ground grass texture
- asphalt.png/jpg - Track asphalt texture
- sky_sunset.png/jpg - Sky texture

## Models (game/assets/models/)

- car.obj/fbx - Car 3D model (optional, uses cube by default)
- track.obj/fbx - Track 3D model (optional, generated procedurally)

## Sounds (game/assets/sounds/)

- engine.wav/ogg - Engine sound
- drift.wav/ogg - Drift/skid sound
- boost.wav/ogg - Boost power-up sound
- music.wav/ogg - Background music
- countdown.wav/ogg - Race countdown sound

## Usage in Code

Assets are referenced by name without extension in most cases.
Ursina will automatically find the correct file.

Example:

```python
Entity(texture='grass')  # Finds grass.png or grass.jpg
Entity(model='car')      # Finds car.obj or car.fbx
Audio('engine')          # Finds engine.wav or engine.ogg
```
