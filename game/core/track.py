"""Track system with boundaries and spawn points."""

from ursina import *
from game import config
from game.core.checkpoints import CheckpointSystem


class Track:
    """Represents a race track with mesh, boundaries, and spawn points."""

    def __init__(self, track_name="default"):
        """Initialize the track."""
        self.name = track_name

        # Create track mesh
        self.ground = Entity(
            model="plane",
            scale=(100, 1, 100),
            texture="grass",
            collider="box",
            color=color.rgb(100, 200, 100),
        )

        # Create track surface
        self.track_surface = self.create_track_surface()

        # Boundaries
        self.boundaries = self.create_boundaries()

        # Spawn points
        self.spawn_points = self.create_spawn_points()

        # Checkpoint system
        self.checkpoint_system = CheckpointSystem()

        # Track properties
        self.lap_length = 1000.0

    def create_track_surface(self):
        """Create the main track surface."""
        # Simple oval track for now
        track = Entity(
            model="cube",
            scale=(80, 0.1, 40),
            position=(0, 0.05, 0),
            texture="asphalt",
            color=color.rgb(40, 40, 40),
            collider="box",
        )
        return track

    def create_boundaries(self):
        """Create track boundaries/walls."""
        boundaries = []

        # Outer walls
        positions = [
            (0, 1, 25, (85, 2, 1)),  # North wall
            (0, 1, -25, (85, 2, 1)),  # South wall
            (42.5, 1, 0, (1, 2, 50)),  # East wall
            (-42.5, 1, 0, (1, 2, 50)),  # West wall
        ]

        for x, y, z, scale in positions:
            wall = Entity(
                model="cube",
                position=(x, y, z),
                scale=scale,
                color=color.rgb(200, 50, 50),
                collider="box",
            )
            boundaries.append(wall)

        return boundaries

    def create_spawn_points(self):
        """Create spawn points for players."""
        spawn_points = []

        # Grid of spawn points
        for i in range(config.MAX_PLAYERS):
            row = i // 2
            col = i % 2
            spawn_points.append(
                {
                    "position": Vec3(-5 + col * 10, 1, -15 + row * 5),
                    "rotation": Vec3(0, 0, 0),
                }
            )

        return spawn_points

    def get_spawn_point(self, index):
        """Get spawn point by index."""
        if 0 <= index < len(self.spawn_points):
            return self.spawn_points[index]
        return self.spawn_points[0]

    def is_out_of_bounds(self, position):
        """Check if position is out of bounds."""
        x, z = position.x, position.z
        return abs(x) > 50 or abs(z) > 30

    def get_nearest_track_position(self, position):
        """Get nearest valid position on track."""
        x = clamp(position.x, -40, 40)
        z = clamp(position.z, -20, 20)
        return Vec3(x, position.y, z)

    def cleanup(self):
        """Clean up track resources."""
        destroy(self.ground)
        destroy(self.track_surface)
        for boundary in self.boundaries:
            destroy(boundary)
