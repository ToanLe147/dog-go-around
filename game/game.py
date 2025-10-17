"""Main game application using Pyglet."""

import sys
import pyglet
from pyglet.window import key, mouse
from game import config


class Game:
    """Main game class."""

    def __init__(self, offline_mode=False, player_name="Player1"):
        """Initialize the game."""
        # Create window
        self.window = pyglet.window.Window(
            width=config.WINDOW_WIDTH,
            height=config.WINDOW_HEIGHT,
            caption=config.WINDOW_TITLE,
            fullscreen=config.FULLSCREEN,
        )
        self.window.push_handlers(self)
        self.clock = pyglet.clock

        # Game state
        self.running = True
        self.state = "menu"  # menu, racing, paused, results
        self.offline_mode = offline_mode
        self.player_name = player_name

        # Initialize subsystems
        from game.core.car import Car
        from game.core.track import Track
        from game.ui.menu import Menu
        from game.ui.hud import HUD

        self.track = Track()
        self.player_car = Car(100, 100, config.COLOR_PLAYER, is_player=True)
        self.menu = Menu(self.window)
        self.hud = HUD(self.window)
        self.cars = [self.player_car]

        # Key state handler for polling
        self.keys = key.KeyStateHandler()
        self.window.push_handlers(self.keys)

        # Camera offset for following player
        self.camera_x = 0
        self.camera_y = 0

    def run(self):
        """Main game loop: schedule updates and start pyglet app."""
        self.clock.schedule_interval(self._update, 1.0 / config.FPS)
        pyglet.app.run()
        sys.exit()

    # Pyglet event handlers
    def on_close(self):
        pyglet.app.exit()

    def on_key_press(self, symbol, modifiers):
        if self.state == "menu":
            action = self.menu.on_key_press(symbol)
            if action == "start":
                self.start_race()
            elif action == "quit":
                pyglet.app.exit()
        elif self.state == "racing":
            if symbol == key.ESCAPE:
                self.state = "paused"
        elif self.state == "paused":
            if symbol == key.ESCAPE:
                self.state = "racing"
            elif symbol == key.Q:
                self.state = "menu"

    def on_mouse_press(self, x, y, button, modifiers):
        if self.state == "menu":
            action = self.menu.on_mouse_press(x, y, button)
            if action == "start":
                self.start_race()
            elif action == "quit":
                pyglet.app.exit()

    def _update(self, dt):
        """Scheduled update function for pyglet."""
        if self.state == "racing":
            # Input flags
            k = key
            accel = self.keys[k.W] or self.keys[k.UP]
            brake = self.keys[k.S] or self.keys[k.DOWN]
            left = self.keys[k.A] or self.keys[k.LEFT]
            right = self.keys[k.D] or self.keys[k.RIGHT]

            # Update player car
            self.player_car.update(dt, accel, brake, left, right, self.track)

            # Camera follow
            self.camera_x = self.player_car.x - config.WINDOW_WIDTH // 2
            self.camera_y = self.player_car.y - config.WINDOW_HEIGHT // 2

            # Update HUD
            self.hud.update(self.player_car)

    def on_draw(self):
        self.window.clear()
        batch = pyglet.graphics.Batch()

        if self.state == "menu":
            # Background
            try:
                bg = pyglet.shapes.Rectangle(
                    0,
                    0,
                    config.WINDOW_WIDTH,
                    config.WINDOW_HEIGHT,
                    color=config.COLOR_BACKGROUND,
                    batch=batch,
                )
            except Exception:
                pass
            self.menu.render(batch)
        elif self.state in ["racing", "paused"]:
            # Background
            try:
                bg = pyglet.shapes.Rectangle(
                    0,
                    0,
                    config.WINDOW_WIDTH,
                    config.WINDOW_HEIGHT,
                    color=config.COLOR_BACKGROUND,
                    batch=batch,
                )
            except Exception:
                pass
            self.track.render(batch, self.camera_x, self.camera_y)
            for car in self.cars:
                car.render(batch, self.camera_x, self.camera_y)
            self.hud.render()
            if self.state == "paused":
                self.render_pause_overlay()
        batch.draw()

    def start_race(self):
        """Start a new race."""
        self.state = "racing"
        self.player_car.reset(100, 100)

    def render_pause_overlay(self):
        """Render pause menu overlay."""
        # Simple pause overlay text using pyglet labels
        label = pyglet.text.Label(
            "PAUSED",
            font_name=None,
            font_size=48,
            x=config.WINDOW_WIDTH // 2,
            y=config.WINDOW_HEIGHT // 2,
            anchor_x="center",
            anchor_y="center",
            color=(255, 255, 255, 255),
        )
        label.draw()
