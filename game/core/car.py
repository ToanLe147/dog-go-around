"""Player vehicle entity with physics."""

from ursina import *
from game import config
from game.core.physics import Physics
from game.utils.input_map import InputMap


class Car:
    """Player vehicle with movement, collision, and effects."""

    def __init__(self, position=Vec3(0, 1, 0), rotation=Vec3(0, 0, 0), is_remote=False):
        """Initialize the car."""
        self.is_remote = is_remote

        # Create car entity
        self.entity = Entity(
            model="cube",
            color=color.rgb(0, 100, 255),
            scale=(2, 1, 4),
            position=position,
            rotation=rotation,
            collider="box",
        )

        # Physics component
        self.physics = Physics(self.entity)

        # Car properties
        self.speed = 0.0
        self.max_speed = config.MAX_SPEED
        self.boost_active = False
        self.boost_timer = 0.0

        # Input handling (only for local player)
        if not is_remote:
            self.input_map = InputMap()
        else:
            self.input_map = None

        # Effects
        self.setup_effects()

    def setup_effects(self):
        """Set up visual effects."""
        # Exhaust particles (placeholder)
        self.exhaust = Entity(
            parent=self.entity,
            model="sphere",
            scale=0.3,
            position=(0, -0.3, -2),
            color=color.smoke,
            visible=False,
        )

        # Boost trail
        self.boost_trail = Entity(
            parent=self.entity,
            model="quad",
            scale=(1, 0.1, 3),
            position=(0, -0.4, -2),
            color=color.orange,
            visible=False,
        )

    def update(self):
        """Update car state."""
        if self.is_remote:
            return  # Remote cars are updated by network sync

        # Get input
        throttle = 0.0
        steer = 0.0
        brake = False
        handbrake = False
        boost = False

        if self.input_map:
            if held_keys["w"] or held_keys["up arrow"]:
                throttle = 1.0
            if held_keys["s"] or held_keys["down arrow"]:
                throttle = -1.0
                brake = True
            if held_keys["a"] or held_keys["left arrow"]:
                steer = -1.0
            if held_keys["d"] or held_keys["right arrow"]:
                steer = 1.0
            if held_keys["space"]:
                handbrake = True
            if held_keys["left shift"]:
                boost = True

            # Reset car
            if held_keys["r"]:
                self.reset()

        # Apply physics
        self.physics.apply_input(throttle, steer, brake, handbrake, boost)
        self.physics.update()

        # Update speed
        self.speed = self.physics.get_speed()

        # Update boost
        if boost and self.boost_timer <= 0:
            self.boost_active = True
            self.boost_timer = config.BOOST_DURATION

        if self.boost_timer > 0:
            self.boost_timer -= time.dt
            self.boost_trail.visible = True
        else:
            self.boost_active = False
            self.boost_trail.visible = False

        # Update effects
        self.exhaust.visible = throttle > 0

    def reset(self):
        """Reset car to spawn position."""
        self.entity.position = Vec3(0, 1, 0)
        self.entity.rotation = Vec3(0, 0, 0)
        self.physics.reset()
        self.speed = 0.0

    def get_position(self):
        """Get car position."""
        return self.entity.position

    def get_rotation(self):
        """Get car rotation."""
        return self.entity.rotation

    def get_velocity(self):
        """Get car velocity."""
        return self.physics.velocity

    def set_position(self, position):
        """Set car position (for network sync)."""
        self.entity.position = position

    def set_rotation(self, rotation):
        """Set car rotation (for network sync)."""
        self.entity.rotation = rotation

    def set_velocity(self, velocity):
        """Set car velocity (for network sync)."""
        self.physics.velocity = velocity
