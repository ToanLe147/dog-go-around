"""Math utilities and helpers."""

import math
from typing import Tuple


class MathUtils:
    """Mathematical utility functions."""

    @staticmethod
    def clamp(value: float, min_val: float, max_val: float) -> float:
        """Clamp value between min and max."""
        return max(min_val, min(max_val, value))

    @staticmethod
    def lerp(a: float, b: float, t: float) -> float:
        """Linear interpolation between a and b."""
        return a + (b - a) * t

    @staticmethod
    def inverse_lerp(a: float, b: float, value: float) -> float:
        """Inverse linear interpolation."""
        if abs(b - a) < 1e-6:
            return 0.0
        return (value - a) / (b - a)

    @staticmethod
    def remap(
        value: float, in_min: float, in_max: float, out_min: float, out_max: float
    ) -> float:
        """Remap value from one range to another."""
        t = MathUtils.inverse_lerp(in_min, in_max, value)
        return MathUtils.lerp(out_min, out_max, t)

    @staticmethod
    def smooth_step(t: float) -> float:
        """Smooth step interpolation (0 to 1)."""
        t = MathUtils.clamp(t, 0.0, 1.0)
        return t * t * (3.0 - 2.0 * t)

    @staticmethod
    def smoother_step(t: float) -> float:
        """Smoother step interpolation (0 to 1)."""
        t = MathUtils.clamp(t, 0.0, 1.0)
        return t * t * t * (t * (t * 6.0 - 15.0) + 10.0)

    @staticmethod
    def angle_difference(a: float, b: float) -> float:
        """Get shortest difference between two angles."""
        diff = (b - a) % 360
        if diff > 180:
            diff -= 360
        return diff

    @staticmethod
    def wrap_angle(angle: float) -> float:
        """Wrap angle to -180 to 180 range."""
        while angle > 180:
            angle -= 360
        while angle < -180:
            angle += 360
        return angle

    @staticmethod
    def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate 2D distance between two points."""
        dx = x2 - x1
        dy = y2 - y1
        return math.sqrt(dx * dx + dy * dy)

    @staticmethod
    def distance_3d(
        x1: float, y1: float, z1: float, x2: float, y2: float, z2: float
    ) -> float:
        """Calculate 3D distance between two points."""
        dx = x2 - x1
        dy = y2 - y1
        dz = z2 - z1
        return math.sqrt(dx * dx + dy * dy + dz * dz)

    @staticmethod
    def normalize_vector_2d(x: float, y: float) -> Tuple[float, float]:
        """Normalize a 2D vector."""
        length = math.sqrt(x * x + y * y)
        if length < 1e-6:
            return 0.0, 0.0
        return x / length, y / length

    @staticmethod
    def normalize_vector_3d(x: float, y: float, z: float) -> Tuple[float, float, float]:
        """Normalize a 3D vector."""
        length = math.sqrt(x * x + y * y + z * z)
        if length < 1e-6:
            return 0.0, 0.0, 0.0
        return x / length, y / length, z / length

    @staticmethod
    def dot_product_2d(x1: float, y1: float, x2: float, y2: float) -> float:
        """Calculate 2D dot product."""
        return x1 * x2 + y1 * y2

    @staticmethod
    def dot_product_3d(
        x1: float, y1: float, z1: float, x2: float, y2: float, z2: float
    ) -> float:
        """Calculate 3D dot product."""
        return x1 * x2 + y1 * y2 + z1 * z2

    @staticmethod
    def sign(value: float) -> int:
        """Get sign of value (-1, 0, or 1)."""
        if value > 0:
            return 1
        elif value < 0:
            return -1
        return 0

    @staticmethod
    def ease_in_quad(t: float) -> float:
        """Quadratic ease-in."""
        return t * t

    @staticmethod
    def ease_out_quad(t: float) -> float:
        """Quadratic ease-out."""
        return t * (2.0 - t)

    @staticmethod
    def ease_in_out_quad(t: float) -> float:
        """Quadratic ease-in-out."""
        if t < 0.5:
            return 2.0 * t * t
        return -1.0 + (4.0 - 2.0 * t) * t
