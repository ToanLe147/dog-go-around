"""HUD (Heads-Up Display) for racing."""

import pygame
from game import config


class HUD:
    """In-game HUD showing speed, lap info, etc."""

    def __init__(self, screen):
        """Initialize HUD."""
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 28)

        # Stats
        self.speed = 0
        self.lap = 1
        self.position = 1

    def update(self, player_car):
        """Update HUD stats."""
        self.speed = abs(player_car.speed)

    def render(self):
        """Render HUD elements."""
        # Speed display
        speed_text = self.font.render(
            f"Speed: {int(self.speed)} km/h", True, config.COLOR_TEXT
        )

        # Create semi-transparent background
        speed_bg = pygame.Surface(
            (speed_text.get_width() + 20, speed_text.get_height() + 10)
        )
        speed_bg.set_alpha(180)
        speed_bg.fill((0, 0, 0))

        self.screen.blit(speed_bg, (10, 10))
        self.screen.blit(speed_text, (20, 15))

        # Lap counter
        lap_text = self.font.render(f"Lap: {self.lap}/3", True, config.COLOR_TEXT)
        lap_bg = pygame.Surface((lap_text.get_width() + 20, lap_text.get_height() + 10))
        lap_bg.set_alpha(180)
        lap_bg.fill((0, 0, 0))

        self.screen.blit(lap_bg, (10, 60))
        self.screen.blit(lap_text, (20, 65))

        # Position
        position_text = self.font.render(
            f"Position: {self.position}", True, config.COLOR_TEXT
        )
        position_bg = pygame.Surface(
            (position_text.get_width() + 20, position_text.get_height() + 10)
        )
        position_bg.set_alpha(180)
        position_bg.fill((0, 0, 0))

        self.screen.blit(position_bg, (10, 110))
        self.screen.blit(position_text, (20, 115))

        # Controls hint
        controls = [
            "W/↑ - Accelerate",
            "S/↓ - Brake",
            "A/← - Turn Left",
            "D/→ - Turn Right",
            "ESC - Pause",
        ]

        y_offset = config.WINDOW_HEIGHT - 160
        for control in controls:
            control_text = self.font_small.render(control, True, config.COLOR_TEXT)
            control_bg = pygame.Surface(
                (control_text.get_width() + 10, control_text.get_height() + 4)
            )
            control_bg.set_alpha(150)
            control_bg.fill((0, 0, 0))

            self.screen.blit(control_bg, (10, y_offset))
            self.screen.blit(control_text, (15, y_offset + 2))
            y_offset += 30
