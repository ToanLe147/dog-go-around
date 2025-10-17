"""Tests for physics functionality."""

import pytest
from ursina import Vec3, Entity


class MockEntity:
    """Mock entity for testing."""

    def __init__(self):
        self.position = Vec3(0, 1, 0)
        self.rotation = Vec3(0, 0, 0)
        self.rotation_y = 0
        self.forward = Vec3(0, 0, 1)
        self.right = Vec3(1, 0, 0)
        self.up = Vec3(0, 1, 0)


class TestPhysics:
    """Test physics engine."""

    def test_physics_initialization(self):
        """Test physics component initialization."""
        from game.core.physics import Physics

        entity = MockEntity()
        physics = Physics(entity)

        assert physics.velocity == Vec3(0, 0, 0)
        assert physics.acceleration == Vec3(0, 0, 0)
        assert physics.mass == 1000.0

    def test_get_speed(self):
        """Test speed calculation."""
        from game.core.physics import Physics

        entity = MockEntity()
        physics = Physics(entity)

        # Set velocity
        physics.velocity = Vec3(3, 0, 4)

        # Speed should be magnitude of velocity
        assert physics.get_speed() == 5.0

    def test_reset(self):
        """Test physics reset."""
        from game.core.physics import Physics

        entity = MockEntity()
        physics = Physics(entity)

        # Set some values
        physics.velocity = Vec3(10, 5, 10)
        physics.acceleration = Vec3(1, 1, 1)
        physics.is_drifting = True

        # Reset
        physics.reset()

        assert physics.velocity == Vec3(0, 0, 0)
        assert physics.acceleration == Vec3(0, 0, 0)
        assert physics.is_drifting is False


class TestCheckpoints:
    """Test checkpoint system."""

    def test_checkpoint_creation(self):
        """Test checkpoint initialization."""
        from game.core.checkpoints import Checkpoint

        checkpoint = Checkpoint(0, Vec3(0, 0, 0), 5.0)

        assert checkpoint.index == 0
        assert checkpoint.position == Vec3(0, 0, 0)
        assert checkpoint.radius == 5.0

    def test_checkpoint_inside(self):
        """Test checkpoint collision detection."""
        from game.core.checkpoints import Checkpoint

        checkpoint = Checkpoint(0, Vec3(0, 0, 0), 5.0)

        # Position inside
        assert checkpoint.is_inside(Vec3(0, 0, 0)) is True
        assert checkpoint.is_inside(Vec3(3, 0, 0)) is True

        # Position outside
        assert checkpoint.is_inside(Vec3(10, 0, 0)) is False
        assert checkpoint.is_inside(Vec3(0, 10, 0)) is False

    def test_checkpoint_system_progress(self):
        """Test checkpoint system progression."""
        from game.core.checkpoints import CheckpointSystem

        system = CheckpointSystem()

        # Should start at checkpoint 0
        assert system.current_checkpoint == 0
        assert system.lap_complete is False

        # Pass through checkpoints
        for checkpoint in system.checkpoints:
            system.check_checkpoint(checkpoint.position)

        # Lap should be complete after all checkpoints
        assert system.lap_complete is True


class TestMathUtils:
    """Test math utilities."""

    def test_clamp(self):
        """Test clamping values."""
        from game.utils.mathx import MathUtils

        assert MathUtils.clamp(5, 0, 10) == 5
        assert MathUtils.clamp(-5, 0, 10) == 0
        assert MathUtils.clamp(15, 0, 10) == 10

    def test_lerp(self):
        """Test linear interpolation."""
        from game.utils.mathx import MathUtils

        assert MathUtils.lerp(0, 10, 0.0) == 0
        assert MathUtils.lerp(0, 10, 0.5) == 5
        assert MathUtils.lerp(0, 10, 1.0) == 10

    def test_distance_2d(self):
        """Test 2D distance calculation."""
        from game.utils.mathx import MathUtils

        # Distance between (0,0) and (3,4) should be 5
        assert MathUtils.distance_2d(0, 0, 3, 4) == 5.0

    def test_normalize_vector_2d(self):
        """Test 2D vector normalization."""
        from game.utils.mathx import MathUtils

        x, y = MathUtils.normalize_vector_2d(3, 4)

        # Length should be 1
        length = (x**2 + y**2) ** 0.5
        assert abs(length - 1.0) < 0.0001


class TestTiming:
    """Test timing utilities."""

    def test_timer_start_stop(self):
        """Test timer start and stop."""
        from game.utils.timing import Timer
        import time

        timer = Timer()
        timer.start()

        assert timer.running is True

        time.sleep(0.1)

        timer.stop()

        assert timer.running is False
        assert timer.get_elapsed() >= 0.1

    def test_timer_pause_resume(self):
        """Test timer pause and resume."""
        from game.utils.timing import Timer
        import time

        timer = Timer()
        timer.start()
        time.sleep(0.1)

        timer.pause()
        assert timer.paused is True

        paused_time = timer.get_elapsed()
        time.sleep(0.1)  # Time shouldn't advance while paused

        timer.resume()
        assert timer.paused is False

        # Time should be close to paused time
        assert abs(timer.get_elapsed() - paused_time) < 0.05


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
