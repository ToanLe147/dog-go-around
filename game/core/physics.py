"""Physics engine for vehicle movement."""

from ursina import *
from game import config


class Physics:
    """Handles acceleration, steering, friction, drift, and reset."""

    def __init__(self, entity):
        """Initialize physics for an entity."""
        self.entity = entity

        # Velocity and forces
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)

        # Physics properties
        self.mass = 1000.0
        self.max_speed = config.MAX_SPEED
        self.acceleration_force = config.ACCELERATION
        self.brake_force = config.BRAKE_FORCE
        self.turn_speed = config.TURN_SPEED
        self.friction = config.FRICTION
        self.air_resistance = config.AIR_RESISTANCE
        self.drift_factor = config.DRIFT_FACTOR

        # State
        self.is_drifting = False
        self.is_on_ground = True
        self.boost_active = False

    def apply_input(self, throttle, steer, brake, handbrake, boost):
        """Apply input forces."""
        # Forward/backward acceleration
        if throttle != 0:
            forward_force = self.entity.forward * throttle * self.acceleration_force
            self.acceleration += forward_force

        # Braking
        if brake:
            brake_force = -self.velocity.normalized() * self.brake_force
            self.acceleration += brake_force

        # Steering (only when moving)
        speed = self.get_speed()
        if speed > 0.1 and steer != 0:
            turn_amount = steer * self.turn_speed * time.dt
            # Scale turn speed with velocity
            turn_amount *= min(1.0, speed / 10.0)
            self.entity.rotation_y += turn_amount

        # Handbrake (drifting)
        if handbrake and speed > 5:
            self.is_drifting = True
            # Reduce lateral friction
            lateral = self.entity.right
            lateral_velocity = self.velocity.dot(lateral) * lateral
            self.velocity -= lateral_velocity * (1 - self.drift_factor) * time.dt
        else:
            self.is_drifting = False

        # Boost
        if boost:
            self.boost_active = True
            boost_force = (
                self.entity.forward * config.BOOST_MULTIPLIER * self.acceleration_force
            )
            self.acceleration += boost_force
        else:
            self.boost_active = False

    def update(self):
        """Update physics simulation."""
        # Apply gravity
        if not self.is_on_ground:
            self.velocity.y += config.GRAVITY * time.dt

        # Apply acceleration
        self.velocity += self.acceleration * time.dt

        # Apply friction
        if self.is_on_ground:
            self.velocity *= self.friction

        # Apply air resistance
        self.velocity *= self.air_resistance

        # Clamp speed
        speed = self.get_speed()
        if speed > self.max_speed:
            self.velocity = self.velocity.normalized() * self.max_speed

        # Update position
        self.entity.position += self.velocity * time.dt

        # Ground check (simple)
        if self.entity.position.y < 1:
            self.entity.position.y = 1
            self.velocity.y = 0
            self.is_on_ground = True
        else:
            self.is_on_ground = False

        # Reset acceleration
        self.acceleration = Vec3(0, 0, 0)

    def get_speed(self):
        """Get current speed (magnitude of velocity)."""
        return self.velocity.length()

    def reset(self):
        """Reset physics state."""
        self.velocity = Vec3(0, 0, 0)
        self.acceleration = Vec3(0, 0, 0)
        self.is_drifting = False

    def apply_force(self, force):
        """Apply an external force."""
        self.acceleration += force / self.mass

    def set_position(self, position):
        """Set entity position."""
        self.entity.position = position
