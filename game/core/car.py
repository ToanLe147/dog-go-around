"""Car entity with simple 2D physics (framework-agnostic)."""

import math
from game import config
from pyglet import shapes


class Car:
    """Represents a car in the game."""

    def __init__(self, x, y, color, is_player=False):
        """Initialize the car."""
        self.x = float(x)
        self.y = float(y)
        self.angle = 0.0  # degrees
        self.speed = 0.0
        self.color = color
        self.is_player = is_player

        # Car dimensions (pixels)
        self.width = 30
        self.height = 50

        # Velocity components (pixels/sec)
        self.vx = 0.0
        self.vy = 0.0

    def update(
        self, dt, accelerating, braking, turning_left, turning_right, track=None
    ):
        """Update car physics and position.

        Args:
            dt: Delta time in seconds.
            accelerating: True if throttle pressed.
            braking: True if brake/reverse pressed.
            turning_left: True if steering left.
            turning_right: True if steering right.
            track: Optional track reference (unused for now).
        """
        if not self.is_player:
            return

        # Apply acceleration / brake
        if accelerating:
            self.speed += config.ACCELERATION * dt
        elif braking:
            self.speed -= config.ACCELERATION * 0.5 * dt

        # Friction
        self.speed *= config.FRICTION

        # Clamp
        self.speed = max(-config.MAX_SPEED * 0.5, min(config.MAX_SPEED, self.speed))

        # Turning (stronger when faster)
        if abs(self.speed) > 10:
            turn = config.TURN_SPEED * dt * (abs(self.speed) / config.MAX_SPEED)
            if turning_left:
                self.angle -= turn
            if turning_right:
                self.angle += turn

        # Velocity from angle
        ang = math.radians(self.angle)
        self.vx = math.sin(ang) * self.speed
        self.vy = -math.cos(ang) * self.speed

        # Integrate position
        self.x += self.vx * dt
        self.y += self.vy * dt

    def reset(self, x, y):
        """Reset car to starting position."""
        self.x = float(x)
        self.y = float(y)
        self.angle = 0.0
        self.speed = 0.0
        self.vx = 0.0
        self.vy = 0.0

    def render(self, batch, camera_x, camera_y):
        """Render the car using a rotated rectangle in pyglet and return it."""

        screen_x = self.x - camera_x
        screen_y = self.y - camera_y

        rect = shapes.Rectangle(
            screen_x, screen_y, self.width, self.height, color=self.color, batch=batch
        )
        # rotate around center
        rect.anchor_position = (self.width / 2, self.height / 2)
        rect.rotation = self.angle
        return rect
