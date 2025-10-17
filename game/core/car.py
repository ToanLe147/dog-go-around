"""Car entity with simple 2D physics for Pygame."""

import math
import pygame
from game import config


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

    def update(self, dt, keys, track):
        """Update car physics and position."""
        if not self.is_player:
            return

        # Input handling
        accelerating = keys[pygame.K_w] or keys[pygame.K_UP]
        braking = keys[pygame.K_s] or keys[pygame.K_DOWN]
        turning_left = keys[pygame.K_a] or keys[pygame.K_LEFT]
        turning_right = keys[pygame.K_d] or keys[pygame.K_RIGHT]

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

    def render(self, screen, camera_x, camera_y):
        """Render the car."""
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)

        # Car surface
        surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(surf, self.color, (0, 0, self.width, self.height))
        pygame.draw.rect(surf, (255, 255, 255), (0, 0, self.width, self.height), 2)
        # Direction arrow
        pygame.draw.polygon(
            surf,
            (255, 255, 0),
            [
                (self.width // 2, 5),
                (self.width // 2 - 8, 20),
                (self.width // 2 + 8, 20),
            ],
        )

        rotated = pygame.transform.rotate(surf, -self.angle)
        rect = rotated.get_rect(center=(screen_x, screen_y))
        screen.blit(rotated, rect)
