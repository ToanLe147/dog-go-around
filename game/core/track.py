"""Track rendering and collision for Pyglet.

Provides an oval track with inner/outer boundaries, dashed center line,
and visual checkpoints. Includes a helper to test if a point lies on the
drivable band of the track.
"""

import math
import pyglet
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
        """Render the track using pyglet shapes and lines into the given batch."""
        # Build vertex lists for polygons (outer and inner)
        outer = []
        for x, y in self.outer_points:
            outer.extend([x - camera_x, y - camera_y])
        inner = []
        for x, y in self.inner_points:
            inner.extend([x - camera_x, y - camera_y])

        # Filled outer polygon (approximation via triangle fan)
        if len(outer) >= 6:
            pyglet.graphics.draw(
                len(outer) // 2,
                pyglet.gl.GL_TRIANGLE_FAN,
                ("v2f", outer),
                ("c3B", list(config.COLOR_TRACK) * (len(outer) // 2)),
            )

        # Inner cut-out (draw background over inner to simulate hole)
        if len(inner) >= 6:
            pyglet.graphics.draw(
                len(inner) // 2,
                pyglet.gl.GL_TRIANGLE_FAN,
                ("v2f", inner),
                ("c3B", list(config.COLOR_BACKGROUND) * (len(inner) // 2)),
            )

        # Borders as line loops
        if len(outer) >= 6:
            pyglet.graphics.draw(
                len(outer) // 2,
                pyglet.gl.GL_LINE_LOOP,
                ("v2f", outer),
                ("c3B", list(config.COLOR_TRACK_BORDER) * (len(outer) // 2)),
            )
        if len(inner) >= 6:
            pyglet.graphics.draw(
                len(inner) // 2,
                pyglet.gl.GL_LINE_LOOP,
                ("v2f", inner),
                ("c3B", list(config.COLOR_TRACK_BORDER) * (len(inner) // 2)),
            )

        # Dashed center line
        center_points = []
        for i in range(len(self.outer_points)):
            ox, oy = self.outer_points[i]
            ix, iy = self.inner_points[i]
            center_points.append((ox + ix) / 2 - camera_x)
            center_points.append((oy + iy) / 2 - camera_y)

        # draw small segments to simulate dashes
        for i in range(0, len(center_points) - 2, 8):
            x1, y1 = center_points[i], center_points[i + 1]
            x2, y2 = center_points[i + 2], center_points[i + 3]
            pyglet.graphics.draw(
                2,
                pyglet.gl.GL_LINES,
                ("v2f", [x1, y1, x2, y2]),
                ("c3B", [255, 255, 255, 255, 255, 255]),
            )

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

    def is_on_track(self, x, y):
        """Check if a world point (x,y) is on the drivable band of the ellipse."""
        dx = x - self.center_x
        dy = y - self.center_y
        # Ellipse equation normalized distance
        norm = math.sqrt((dx / self.radius_x) ** 2 + (dy / self.radius_y) ** 2)
        inner_bound = (self.radius_x - config.TRACK_WIDTH) / self.radius_x
        outer_bound = (self.radius_x + config.TRACK_WIDTH) / self.radius_x
        return inner_bound <= norm <= outer_bound
