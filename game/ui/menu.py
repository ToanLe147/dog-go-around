"""Main menu interface."""

from ursina import *


class MainMenu:
    """Main menu with start, options, and quit."""

    def __init__(self, app):
        """Initialize main menu."""
        self.app = app

        # Menu panel
        self.panel = Entity(parent=camera.ui, enabled=False)

        # Title
        self.title = Text(
            parent=self.panel,
            text="DOG GO AROUND",
            position=(0, 0.3),
            origin=(0, 0),
            scale=3,
            color=color.gold,
        )

        # Subtitle
        self.subtitle = Text(
            parent=self.panel,
            text="Multiplayer Racing Game",
            position=(0, 0.2),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )

        # Start button
        self.start_button = Button(
            parent=self.panel,
            text="Start Race",
            color=color.rgb(0, 150, 0),
            scale=(0.3, 0.08),
            position=(0, 0),
            on_click=self.on_start_click,
        )

        # Options button
        self.options_button = Button(
            parent=self.panel,
            text="Options",
            color=color.rgb(0, 100, 150),
            scale=(0.3, 0.08),
            position=(0, -0.12),
            on_click=self.on_options_click,
        )

        # Quit button
        self.quit_button = Button(
            parent=self.panel,
            text="Quit",
            color=color.rgb(150, 0, 0),
            scale=(0.3, 0.08),
            position=(0, -0.24),
            on_click=self.on_quit_click,
        )

    def on_start_click(self):
        """Handle start button click."""
        self.app.start_race()

    def on_options_click(self):
        """Handle options button click."""
        print("Options menu not implemented yet")

    def on_quit_click(self):
        """Handle quit button click."""
        self.app.quit_game()

    def show(self):
        """Show the menu."""
        self.panel.enabled = True
        mouse.locked = False

    def hide(self):
        """Hide the menu."""
        self.panel.enabled = False
        mouse.locked = True
