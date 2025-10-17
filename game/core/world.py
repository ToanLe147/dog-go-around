"""World management and scene setup."""

from ursina import *
from game import config
from game.core.track import Track
from game.core.car import Car


class World:
    """Manages the game world, track, and entities."""

    def __init__(self, track_name="default"):
        """Initialize the world."""
        self.track_name = track_name

        # Create lighting
        self.setup_lighting()

        # Create track
        self.track = Track(track_name)

        # Create player car
        spawn_point = self.track.get_spawn_point(0)
        self.player_car = Car(
            position=spawn_point["position"], rotation=spawn_point["rotation"]
        )

        # Other cars (for multiplayer)
        self.other_cars = {}

        # Sky
        self.sky = Sky(texture="sky_sunset.png")

    def setup_lighting(self):
        """Set up scene lighting."""
        # Directional light (sun)
        self.sun = DirectionalLight(
            rotation=(45, -45, 0),
            color=color.rgb(255, 253, 220),
            shadows=config.ENABLE_SHADOWS,
        )

        # Ambient light
        self.ambient = AmbientLight(color=color.rgb(150, 150, 180))

    def update(self):
        """Update the world."""
        self.player_car.update()

        for car in self.other_cars.values():
            car.update()

    def add_car(self, player_id, position, rotation):
        """Add another player's car."""
        if player_id not in self.other_cars:
            self.other_cars[player_id] = Car(
                position=position, rotation=rotation, is_remote=True
            )
        return self.other_cars[player_id]

    def remove_car(self, player_id):
        """Remove a player's car."""
        if player_id in self.other_cars:
            destroy(self.other_cars[player_id].entity)
            del self.other_cars[player_id]

    def cleanup(self):
        """Clean up world resources."""
        if self.track:
            self.track.cleanup()
        if self.player_car:
            destroy(self.player_car.entity)
        for car in self.other_cars.values():
            destroy(car.entity)
        self.other_cars.clear()
