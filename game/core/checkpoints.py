"""Checkpoint system for lap validation."""

from ursina import *
from game import config


class CheckpointSystem:
    """Waypoint list, lap validation, wrong-way detection."""

    def __init__(self):
        """Initialize checkpoint system."""
        self.checkpoints = []
        self.current_checkpoint = 0
        self.lap_complete = False

        # Create default checkpoints (oval track)
        self.create_default_checkpoints()

    def create_default_checkpoints(self):
        """Create default checkpoint layout."""
        # Simple oval with 8 checkpoints
        checkpoint_positions = [
            Vec3(0, 1, -15),  # Start/Finish
            Vec3(20, 1, -15),  # Corner 1
            Vec3(35, 1, 0),  # Side 1
            Vec3(20, 1, 15),  # Corner 2
            Vec3(0, 1, 18),  # Far end
            Vec3(-20, 1, 15),  # Corner 3
            Vec3(-35, 1, 0),  # Side 2
            Vec3(-20, 1, -15),  # Corner 4
        ]

        for i, pos in enumerate(checkpoint_positions):
            checkpoint = Checkpoint(i, pos, config.CHECKPOINT_RADIUS)
            self.checkpoints.append(checkpoint)

            # Visual indicator (debug)
            if config.SHOW_CHECKPOINT_DEBUG:
                Entity(
                    model="sphere",
                    position=pos,
                    scale=config.CHECKPOINT_RADIUS,
                    color=color.rgba(0, 255, 0, 100),
                    collider=None,
                )

    def check_checkpoint(self, position):
        """Check if a position passes through the current checkpoint."""
        if not self.checkpoints:
            return False

        current = self.checkpoints[self.current_checkpoint]

        if current.is_inside(position):
            self.current_checkpoint += 1

            # Check if lap is complete
            if self.current_checkpoint >= len(self.checkpoints):
                self.lap_complete = True
                self.current_checkpoint = 0

            return True

        return False

    def is_lap_complete(self):
        """Check if the current lap is complete."""
        return self.lap_complete

    def reset_lap(self):
        """Reset lap completion flag."""
        self.lap_complete = False

    def is_wrong_way(self, position, forward_vector):
        """Check if going in wrong direction."""
        if not self.checkpoints:
            return False

        # Get next checkpoint
        next_checkpoint = self.checkpoints[self.current_checkpoint]

        # Direction to next checkpoint
        to_checkpoint = (next_checkpoint.position - position).normalized()

        # Dot product to check direction
        dot = forward_vector.dot(to_checkpoint)

        # If dot product is negative, going wrong way
        return dot < -0.5

    def get_progress(self):
        """Get lap progress (0.0 to 1.0)."""
        if not self.checkpoints:
            return 0.0
        return self.current_checkpoint / len(self.checkpoints)


class Checkpoint:
    """Individual checkpoint waypoint."""

    def __init__(self, index, position, radius):
        """Initialize checkpoint."""
        self.index = index
        self.position = position
        self.radius = radius

    def is_inside(self, position):
        """Check if position is inside checkpoint."""
        distance = (position - self.position).length()
        return distance < self.radius
