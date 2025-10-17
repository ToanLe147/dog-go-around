"""Power-up system for boost and other abilities."""

from ursina import *
from game import config


class PowerUpSystem:
    """Manages power-ups in the game world."""

    def __init__(self):
        """Initialize power-up system."""
        self.powerups = []
        self.spawn_points = []
        self.respawn_time = 10.0

    def create_spawn_points(self):
        """Create power-up spawn points."""
        positions = [
            Vec3(15, 1, 0),
            Vec3(-15, 1, 0),
            Vec3(0, 1, 10),
            Vec3(0, 1, -10),
        ]

        for pos in positions:
            spawn = PowerUpSpawn(pos, self.respawn_time)
            self.spawn_points.append(spawn)

    def update(self):
        """Update all power-ups."""
        for spawn in self.spawn_points:
            spawn.update()

    def check_collision(self, position, radius=2.0):
        """Check if position collides with any power-up."""
        for spawn in self.spawn_points:
            if spawn.is_active():
                distance = (spawn.position - position).length()
                if distance < radius:
                    powerup = spawn.collect()
                    return powerup
        return None


class PowerUpSpawn:
    """Power-up spawn point."""

    def __init__(self, position, respawn_time):
        """Initialize spawn point."""
        self.position = position
        self.respawn_time = respawn_time
        self.timer = 0.0
        self.active = True

        # Visual representation
        self.entity = Entity(
            model="sphere",
            position=position,
            scale=1,
            color=color.gold,
            collider="sphere",
        )

    def update(self):
        """Update spawn state."""
        if not self.active:
            self.timer -= time.dt
            if self.timer <= 0:
                self.respawn()

    def is_active(self):
        """Check if power-up is available."""
        return self.active

    def collect(self):
        """Collect the power-up."""
        if self.active:
            self.active = False
            self.timer = self.respawn_time
            self.entity.visible = False
            return PowerUp("boost")
        return None

    def respawn(self):
        """Respawn the power-up."""
        self.active = True
        self.entity.visible = True


class PowerUp:
    """Individual power-up item."""

    def __init__(self, powerup_type):
        """Initialize power-up."""
        self.type = powerup_type
        self.duration = 0.0

        if powerup_type == "boost":
            self.duration = config.BOOST_DURATION

    def apply(self, car):
        """Apply power-up effect to car."""
        if self.type == "boost":
            car.boost_active = True
            car.boost_timer = self.duration
