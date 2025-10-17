"""Track rendering and collision for Pyglet.

Provides an oval track with inner/outer boundaries, dashed center line,
and visual checkpoints. Includes a helper to test if a point lies on the
drivable band of the track.
"""

import math
import pyglet
from pyglet import shapes
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

    def render(self, batch, camera_x, camera_y):
        """Render the track using pyglet shapes and lines into the given batch.
        Returns a list of created shape objects so the caller can hold references.
        """
        drawables = []
        # Build point lists for shapes.Polygon
        outer_pts = [(x - camera_x, y - camera_y) for x, y in self.outer_points]
        inner_pts = [(x - camera_x, y - camera_y) for x, y in self.inner_points]

        # Filled outer polygon
        if len(outer_pts) >= 3:
            try:
                poly = shapes.Polygon(*outer_pts, color=config.COLOR_TRACK, batch=batch)
                drawables.append(poly)
            except TypeError:
                # Pyglet may expect a list of tuples
                poly = shapes.Polygon(*outer_pts, batch=batch)
                poly.color = config.COLOR_TRACK
                drawables.append(poly)

        # Inner cut-out by drawing background-colored polygon
        if len(inner_pts) >= 3:
            try:
                poly2 = shapes.Polygon(
                    *inner_pts, color=config.COLOR_BACKGROUND, batch=batch
                )
                drawables.append(poly2)
            except TypeError:
                poly2 = shapes.Polygon(*inner_pts, batch=batch)
                poly2.color = config.COLOR_BACKGROUND
                drawables.append(poly2)

        # Borders
        for pts in (outer_pts, inner_pts):
            if len(pts) >= 2:
                for i in range(len(pts)):
                    x1, y1 = pts[i]
                    x2, y2 = pts[(i + 1) % len(pts)]
                    # Use positional args to support pyglet versions without 'width' kwarg
                    line = shapes.Line(
                        x1, y1, x2, y2, 2, config.COLOR_TRACK_BORDER, batch
                    )
                    drawables.append(line)

        # Dashed center line
        centers = []
        for i in range(len(self.outer_points)):
            ox, oy = self.outer_points[i]
            ix, iy = self.inner_points[i]
            centers.append((ox + ix) / 2 - camera_x)
            centers.append((oy + iy) / 2 - camera_y)
        # draw short segments every few points
        for i in range(0, len(centers) - 2, 8):
            x1, y1 = centers[i], centers[i + 1]
            x2, y2 = centers[i + 2], centers[i + 3]
            line = shapes.Line(x1, y1, x2, y2, 2, (255, 255, 255), batch)
            drawables.append(line)

        # Checkpoints as translucent circles
        for cx, cy in self.checkpoint_points:
            sx = int(cx - camera_x)
            sy = int(cy - camera_y)
            circle = pyglet.shapes.Circle(
                sx,
                sy,
                config.CHECKPOINT_SIZE // 2,
                color=config.COLOR_CHECKPOINT,
                batch=batch,
            )
            try:
                circle.opacity = 80
            except Exception:
                pass
            drawables.append(circle)

        return drawables

    def is_on_track(self, x, y):
        """Check if a world point (x,y) is on the drivable band of the ellipse."""
        dx = x - self.center_x
        dy = y - self.center_y
        # Ellipse equation normalized distance
        norm = math.sqrt((dx / self.radius_x) ** 2 + (dy / self.radius_y) ** 2)
        inner_bound = (self.radius_x - config.TRACK_WIDTH) / self.radius_x
        outer_bound = (self.radius_x + config.TRACK_WIDTH) / self.radius_x
        return inner_bound <= norm <= outer_bound
