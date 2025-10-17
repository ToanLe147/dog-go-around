"""Heads-up display for race information."""

from ursina import *
from game import config


class HUD:
    """Display speedometer, lap counter, position, and timer."""

    def __init__(self, race_manager):
        """Initialize HUD."""
        self.race_manager = race_manager

        # Speedometer
        self.speed_text = Text(
            text="Speed: 0 km/h",
            position=(-0.85, -0.45),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )

        # Lap counter
        self.lap_text = Text(
            text="Lap: 1/3",
            position=(0, 0.45),
            origin=(0, 0),
            scale=2,
            color=color.white,
        )

        # Position
        self.position_text = Text(
            text="Position: 1st",
            position=(0.85, 0.45),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )

        # Timer
        self.timer_text = Text(
            text="Time: 0:00.000",
            position=(0.85, 0.40),
            origin=(0, 0),
            scale=1.2,
            color=color.white,
        )

        # Wrong way indicator
        self.wrong_way_text = Text(
            text="WRONG WAY!",
            position=(0, 0),
            origin=(0, 0),
            scale=3,
            color=color.red,
            visible=False,
        )

        # Countdown
        self.countdown_text = Text(
            text="",
            position=(0, 0),
            origin=(0, 0),
            scale=5,
            color=color.yellow,
            visible=False,
        )

    def update(self):
        """Update HUD elements."""
        if not self.race_manager:
            return

        # Update speed
        speed = self.race_manager.get_player_speed()
        self.speed_text.text = f"Speed: {int(speed * 3.6)} km/h"

        # Update lap
        current_lap = self.race_manager.current_lap
        total_laps = self.race_manager.total_laps
        self.lap_text.text = f"Lap: {current_lap}/{total_laps}"

        # Update position
        position = self.race_manager.get_player_position()
        position_suffix = self.get_position_suffix(position)
        self.position_text.text = f"Position: {position}{position_suffix}"

        # Update timer
        race_time = self.race_manager.get_race_time()
        minutes = int(race_time // 60)
        seconds = int(race_time % 60)
        milliseconds = int((race_time % 1) * 1000)
        self.timer_text.text = f"Time: {minutes}:{seconds:02d}.{milliseconds:03d}"

        # Update wrong way indicator
        if self.race_manager.is_going_wrong_way():
            self.wrong_way_text.visible = True
        else:
            self.wrong_way_text.visible = False

        # Update countdown
        if self.race_manager.state == "countdown":
            countdown = self.race_manager.get_countdown()
            if countdown > 0:
                self.countdown_text.text = str(int(countdown))
                self.countdown_text.visible = True
            else:
                self.countdown_text.text = "GO!"
                self.countdown_text.visible = True
        else:
            self.countdown_text.visible = False

    def get_position_suffix(self, position):
        """Get position suffix (st, nd, rd, th)."""
        if position == 1:
            return "st"
        elif position == 2:
            return "nd"
        elif position == 3:
            return "rd"
        else:
            return "th"

    def show(self):
        """Show HUD."""
        self.speed_text.enabled = True
        self.lap_text.enabled = True
        self.position_text.enabled = True
        self.timer_text.enabled = True

    def hide(self):
        """Hide HUD."""
        self.speed_text.enabled = False
        self.lap_text.enabled = False
        self.position_text.enabled = False
        self.timer_text.enabled = False
        self.wrong_way_text.visible = False
        self.countdown_text.visible = False
