"""Multiplayer lobby interface."""

from ursina import *


class LobbyUI:
    """Lobby system for multiplayer matchmaking."""

    def __init__(self, app):
        """Initialize lobby."""
        self.app = app
        self.ready = False

        # Lobby panel
        self.panel = Entity(parent=camera.ui, enabled=False)

        # Title
        self.title = Text(
            parent=self.panel,
            text="Lobby",
            position=(0, 0.4),
            origin=(0, 0),
            scale=2.5,
            color=color.white,
        )

        # Track selection
        self.track_label = Text(
            parent=self.panel,
            text="Select Track:",
            position=(-0.3, 0.2),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )

        self.track_dropdown = ButtonGroup(
            parent=self.panel,
            options=["Default Track", "Mountain Pass", "City Circuit"],
            position=(0.1, 0.2),
            default="Default Track",
        )

        # Player list
        self.players_label = Text(
            parent=self.panel,
            text="Players:",
            position=(-0.4, 0),
            origin=(0, 0),
            scale=1.5,
            color=color.white,
        )

        self.players_text = Text(
            parent=self.panel,
            text="",
            position=(-0.4, -0.05),
            origin=(0, 0),
            scale=1,
            color=color.light_gray,
        )

        # Ready button
        self.ready_button = Button(
            parent=self.panel,
            text="Ready",
            color=color.rgb(0, 150, 0),
            scale=(0.25, 0.08),
            position=(0, -0.3),
            on_click=self.toggle_ready,
        )

        # Back button
        self.back_button = Button(
            parent=self.panel,
            text="Back",
            color=color.rgb(150, 0, 0),
            scale=(0.25, 0.08),
            position=(0, -0.42),
            on_click=self.on_back,
        )

    def toggle_ready(self):
        """Toggle ready state."""
        self.ready = not self.ready
        if self.ready:
            self.ready_button.text = "Not Ready"
            self.ready_button.color = color.rgb(150, 100, 0)
        else:
            self.ready_button.text = "Ready"
            self.ready_button.color = color.rgb(0, 150, 0)

    def update_players(self, players):
        """Update player list."""
        player_text = "\n".join(
            [f"{p['name']} - {'Ready' if p['ready'] else 'Not Ready'}" for p in players]
        )
        self.players_text.text = player_text

    def on_back(self):
        """Go back to main menu."""
        self.hide()
        self.app.show_menu()

    def show(self):
        """Show the lobby."""
        self.panel.enabled = True
        mouse.locked = False

    def hide(self):
        """Hide the lobby."""
        self.panel.enabled = False
