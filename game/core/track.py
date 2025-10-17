"""Track rendering and collision for Pygame.

Provides an oval track with inner/outer boundaries, dashed center line,
and visual checkpoints. Includes a helper to test if a point lies on the
drivable band of the track.
"""

import math
import pygame
from game import config


class Track:
    """Represents the racing track."""

    def __init__(self):
        """Initialize the track."""
        # Simple oval track parameters
        self.center_x = 640
        self.center_y = 360
        self.radius_x = 400
        self.radius_y = 250

        # Precompute track edges and checkpoints
        self.outer_points = []
        self.inner_points = []
        self.checkpoint_points = []

        num_points = 100
        for i in range(num_points):
            angle = (i / num_points) * 2 * math.pi

            # Outer edge
            outer_x = self.center_x + math.cos(angle) * (
                self.radius_x + config.TRACK_WIDTH
            )
            outer_y = self.center_y + math.sin(angle) * (
                self.radius_y + config.TRACK_WIDTH
            )
            self.outer_points.append((outer_x, outer_y))

            # Inner edge
            inner_x = self.center_x + math.cos(angle) * (
                self.radius_x - config.TRACK_WIDTH
            )
            inner_y = self.center_y + math.sin(angle) * (
                self.radius_y - config.TRACK_WIDTH
            )
            self.inner_points.append((inner_x, inner_y))

            # Checkpoints (every 25 indices ~ 4 checkpoints)
            if i % 25 == 0:
                checkpoint_x = self.center_x + math.cos(angle) * self.radius_x
                checkpoint_y = self.center_y + math.sin(angle) * self.radius_y
                self.checkpoint_points.append((checkpoint_x, checkpoint_y))

    def render(self, screen, camera_x, camera_y):
        """Render the track."""
        # Outer area
        outer_screen_points = [
            (x - camera_x, y - camera_y) for x, y in self.outer_points
        ]
        pygame.draw.polygon(screen, config.COLOR_TRACK, outer_screen_points)

        # Inner cut-out
        inner_screen_points = [
            (x - camera_x, y - camera_y) for x, y in self.inner_points
        ]
        pygame.draw.polygon(screen, config.COLOR_BACKGROUND, inner_screen_points)

        # Borders
        pygame.draw.lines(
            screen, config.COLOR_TRACK_BORDER, True, outer_screen_points, 3
        )
        pygame.draw.lines(
            screen, config.COLOR_TRACK_BORDER, True, inner_screen_points, 3
        )

        # Dashed center line
        center_points = []
        for i in range(len(self.outer_points)):
            ox, oy = self.outer_points[i]
            ix, iy = self.inner_points[i]
            center_points.append(((ox + ix) / 2 - camera_x, (oy + iy) / 2 - camera_y))
        for i in range(0, len(center_points), 4):
            if i + 1 < len(center_points):
                pygame.draw.line(
                    screen, (255, 255, 255), center_points[i], center_points[i + 1], 2
                )

        # Checkpoints
        for cx, cy in self.checkpoint_points:
            sx = int(cx - camera_x)
            sy = int(cy - camera_y)
            pygame.draw.circle(
                screen,
                config.COLOR_CHECKPOINT,
                (sx, sy),
                config.CHECKPOINT_SIZE // 2,
                5,
            )

    def is_on_track(self, x, y):
        """Check if a world point (x,y) is on the drivable band of the ellipse."""
        dx = x - self.center_x
        dy = y - self.center_y
        # Ellipse equation normalized distance
        norm = math.sqrt((dx / self.radius_x) ** 2 + (dy / self.radius_y) ** 2)
        inner_bound = (self.radius_x - config.TRACK_WIDTH) / self.radius_x
        outer_bound = (self.radius_x + config.TRACK_WIDTH) / self.radius_x
        return inner_bound <= norm <= outer_bound
