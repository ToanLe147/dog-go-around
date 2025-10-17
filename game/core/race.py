"""Race management and flow control."""

from ursina import *
from game import config


class RaceManager:
    """Controls race flow: countdown, laps, finish, results."""

    def __init__(self, world):
        """Initialize race manager."""
        self.world = world

        # Race state
        self.state = "countdown"  # countdown, racing, finished
        self.countdown_timer = config.COUNTDOWN_TIME
        self.race_start_time = 0
        self.race_end_time = 0

        # Lap tracking
        self.current_lap = 1
        self.total_laps = config.LAP_COUNT

        # Player standings
        self.player_positions = {}
        self.player_times = {}

    def update(self):
        """Update race state."""
        if self.state == "countdown":
            self.update_countdown()
        elif self.state == "racing":
            self.update_racing()
        elif self.state == "finished":
            pass  # Wait for results screen

    def update_countdown(self):
        """Update countdown timer."""
        self.countdown_timer -= time.dt

        if self.countdown_timer <= 0:
            self.state = "racing"
            self.race_start_time = time.time()

    def update_racing(self):
        """Update during race."""
        # Check checkpoint progress
        if self.world and self.world.track:
            checkpoint_system = self.world.track.checkpoint_system
            player_pos = self.world.player_car.get_position()

            checkpoint_passed = checkpoint_system.check_checkpoint(player_pos)

            if checkpoint_passed:
                # Check if lap completed
                if checkpoint_system.is_lap_complete():
                    self.current_lap += 1
                    checkpoint_system.reset_lap()

                    # Check if race finished
                    if self.current_lap > self.total_laps:
                        self.finish_race()

    def finish_race(self):
        """Finish the race."""
        self.state = "finished"
        self.race_end_time = time.time()

        # Calculate final time
        final_time = self.race_end_time - self.race_start_time

        # Prepare results data
        results = {
            "time": final_time,
            "laps": self.total_laps,
            "position": self.get_player_position(),
        }

        return results

    def get_player_speed(self):
        """Get player car speed."""
        if self.world and self.world.player_car:
            return self.world.player_car.speed
        return 0.0

    def get_player_position(self):
        """Get player race position."""
        # For now, return 1st place (multiplayer would calculate this)
        return 1

    def get_race_time(self):
        """Get current race time."""
        if self.state == "racing":
            return time.time() - self.race_start_time
        elif self.state == "finished":
            return self.race_end_time - self.race_start_time
        return 0.0

    def get_countdown(self):
        """Get countdown timer."""
        return self.countdown_timer

    def is_going_wrong_way(self):
        """Check if player is going the wrong way."""
        if self.world and self.world.track:
            checkpoint_system = self.world.track.checkpoint_system
            player_pos = self.world.player_car.get_position()
            player_forward = self.world.player_car.entity.forward

            return checkpoint_system.is_wrong_way(player_pos, player_forward)
        return False

    def reset(self):
        """Reset race."""
        self.state = "countdown"
        self.countdown_timer = config.COUNTDOWN_TIME
        self.current_lap = 1
        self.race_start_time = 0
        self.race_end_time = 0
