"""Camera controller with multiple modes."""

from ursina import *
from game import config


class CameraRig:
    """Camera controller with follow and bumper camera modes."""

    FOLLOW_MODE = 0
    BUMPER_MODE = 1

    def __init__(self, target):
        """Initialize camera rig."""
        self.target = target  # Car entity to follow
        self.mode = self.FOLLOW_MODE

        # Camera settings
        self.follow_distance = 15
        self.follow_height = 5
        self.bumper_offset = Vec3(0, 1, 2)

        # Smoothing
        self.smooth_speed = 5.0
        self.rotation_smooth = 3.0

        # Current position and rotation
        self.current_position = camera.position
        self.current_rotation = camera.rotation

        # Set initial camera
        camera.fov = config.FOV

    def update(self):
        """Update camera position and rotation."""
        # Toggle camera mode
        if held_keys["c"]:
            self.toggle_mode()

        if self.mode == self.FOLLOW_MODE:
            self.update_follow_camera()
        elif self.mode == self.BUMPER_MODE:
            self.update_bumper_camera()

    def update_follow_camera(self):
        """Update follow camera (third-person)."""
        if not self.target or not self.target.entity:
            return

        # Target position behind and above the car
        forward = self.target.entity.forward
        target_position = (
            self.target.entity.position
            - forward * self.follow_distance
            + Vec3(0, self.follow_height, 0)
        )

        # Smooth camera movement
        camera.position = lerp(
            camera.position, target_position, time.dt * self.smooth_speed
        )

        # Look at car
        camera.look_at(self.target.entity)

    def update_bumper_camera(self):
        """Update bumper camera (first-person)."""
        if not self.target or not self.target.entity:
            return

        # Position at car bumper
        camera.position = (
            self.target.entity.position
            + self.target.entity.up * self.bumper_offset.y
            + self.target.entity.forward * self.bumper_offset.z
        )

        # Match car rotation
        camera.rotation = self.target.entity.rotation

    def toggle_mode(self):
        """Toggle between camera modes."""
        self.mode = (self.mode + 1) % 2
        time.sleep(0.2)  # Prevent rapid toggling

    def set_target(self, target):
        """Set new target to follow."""
        self.target = target
