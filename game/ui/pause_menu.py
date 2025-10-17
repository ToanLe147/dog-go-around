"""Pause menu interface."""

from ursina import *


class PauseMenu:
    """Pause menu displayed during race."""

    def __init__(self, app):
        """Initialize pause menu."""
        self.app = app

        # Semi-transparent background
        self.background = Entity(
            parent=camera.ui,
            model="quad",
            scale=(2, 2),
            color=color.rgba(0, 0, 0, 180),
            z=1,
            enabled=False,
        )

        # Menu panel
        self.panel = Entity(parent=camera.ui, enabled=False)

        # Title
        self.title = Text(
            parent=self.panel,
            text="PAUSED",
            position=(0, 0.3),
            origin=(0, 0),
            scale=3,
            color=color.yellow,
        )

        # Resume button
        self.resume_button = Button(
            parent=self.panel,
            text="Resume",
            color=color.rgb(0, 150, 0),
            scale=(0.3, 0.08),
            position=(0, 0.05),
            on_click=self.on_resume,
        )

        # Restart button
        self.restart_button = Button(
            parent=self.panel,
            text="Restart",
            color=color.rgb(0, 100, 150),
            scale=(0.3, 0.08),
            position=(0, -0.07),
            on_click=self.on_restart,
        )

        # Settings button
        self.settings_button = Button(
            parent=self.panel,
            text="Settings",
            color=color.rgb(100, 100, 100),
            scale=(0.3, 0.08),
            position=(0, -0.19),
            on_click=self.on_settings,
        )

        # Quit button
        self.quit_button = Button(
            parent=self.panel,
            text="Quit to Menu",
            color=color.rgb(150, 0, 0),
            scale=(0.3, 0.08),
            position=(0, -0.31),
            on_click=self.on_quit,
        )

    def on_resume(self):
        """Resume the game."""
        self.app.resume_game()

    def on_restart(self):
        """Restart the race."""
        self.hide()
        self.app.start_race()

    def on_settings(self):
        """Open settings."""
        print("Settings not implemented yet")

    def on_quit(self):
        """Quit to main menu."""
        self.hide()
        if self.app.world:
            self.app.world.cleanup()
        self.app.show_menu()

    def show(self):
        """Show the pause menu."""
        self.background.enabled = True
        self.panel.enabled = True
        mouse.locked = False

    def hide(self):
        """Hide the pause menu."""
        self.background.enabled = False
        self.panel.enabled = False
        mouse.locked = True
