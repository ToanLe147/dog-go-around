"""HUD (Heads-Up Display) rendered with Pyglet labels."""

import pyglet
from game import config


class HUD:
    """In-game HUD showing speed, lap info, etc."""

    def __init__(self, window):
        """Initialize HUD."""
        self.window = window
        self.font_size = 20
        self.small_size = 16

        # Stats
        self.speed = 0
        self.lap = 1
        self.position = 1

    def update(self, player_car):
        """Update HUD stats."""
        self.speed = abs(player_car.speed)

    def render(self):
        """Render HUD elements using pyglet Labels."""
        labels = []

        labels.append(
            pyglet.text.Label(
                f"Speed: {int(self.speed)} km/h",
                font_size=self.font_size,
                x=20,
                y=config.WINDOW_HEIGHT - 30,
                anchor_x="left",
                anchor_y="center",
                color=(255, 255, 255, 255),
            )
        )

        labels.append(
            pyglet.text.Label(
                f"Lap: {self.lap}/3",
                font_size=self.font_size,
                x=20,
                y=config.WINDOW_HEIGHT - 60,
                anchor_x="left",
                anchor_y="center",
                color=(255, 255, 255, 255),
            )
        )

        labels.append(
            pyglet.text.Label(
                f"Position: {self.position}",
                font_size=self.font_size,
                x=20,
                y=config.WINDOW_HEIGHT - 90,
                anchor_x="left",
                anchor_y="center",
                color=(255, 255, 255, 255),
            )
        )

        controls = [
            "W/↑ - Accelerate",
            "S/↓ - Brake",
            "A/← - Turn Left",
            "D/→ - Turn Right",
            "ESC - Pause",
        ]
        y_offset = 40
        for control in controls:
            labels.append(
                pyglet.text.Label(
                    control,
                    font_size=self.small_size,
                    x=20,
                    y=y_offset,
                    anchor_x="left",
                    anchor_y="baseline",
                    color=(255, 255, 255, 200),
                )
            )
            y_offset += 20

        for lbl in labels:
            lbl.draw()
