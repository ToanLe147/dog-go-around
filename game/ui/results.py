"""Race results screen."""

from ursina import *


class ResultsScreen:
    """Display race results and standings."""

    def __init__(self, app):
        """Initialize results screen."""
        self.app = app

        # Panel
        self.panel = Entity(parent=camera.ui, enabled=False)

        # Title
        self.title = Text(
            parent=self.panel,
            text="RACE COMPLETE!",
            position=(0, 0.4),
            origin=(0, 0),
            scale=3,
            color=color.gold,
        )

        # Results text
        self.results_text = Text(
            parent=self.panel,
            text="",
            position=(0, 0.1),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )

        # Position display
        self.position_text = Text(
            parent=self.panel,
            text="",
            position=(0, -0.05),
            origin=(0, 0),
            scale=2,
            color=color.yellow,
        )

        # Time display
        self.time_text = Text(
            parent=self.panel,
            text="",
            position=(0, -0.15),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )

        # Continue button
        self.continue_button = Button(
            parent=self.panel,
            text="Continue",
            color=color.rgb(0, 150, 0),
            scale=(0.3, 0.08),
            position=(0, -0.35),
            on_click=self.on_continue,
        )

    def show(self, results_data):
        """Show results screen with data."""
        self.panel.enabled = True
        mouse.locked = False

        # Format time
        time_val = results_data.get("time", 0)
        minutes = int(time_val // 60)
        seconds = int(time_val % 60)
        milliseconds = int((time_val % 1) * 1000)

        # Update text
        position = results_data.get("position", 1)
        position_suffix = self.get_position_suffix(position)

        self.position_text.text = f"{position}{position_suffix} Place"
        self.time_text.text = f"Time: {minutes}:{seconds:02d}.{milliseconds:03d}"

        # Medal/trophy based on position
        if position == 1:
            self.position_text.color = color.gold
            self.results_text.text = "WINNER! 🏆"
        elif position == 2:
            self.position_text.color = color.rgb(192, 192, 192)  # Silver
            self.results_text.text = "Second Place!"
        elif position == 3:
            self.position_text.color = color.rgb(205, 127, 50)  # Bronze
            self.results_text.text = "Third Place!"
        else:
            self.position_text.color = color.white
            self.results_text.text = "Race Complete"

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

    def on_continue(self):
        """Return to main menu."""
        self.hide()
        if self.app.world:
            self.app.world.cleanup()
        self.app.show_menu()

    def hide(self):
        """Hide the results screen."""
        self.panel.enabled = False
