"""Main menu UI for Pyglet version."""

import pyglet
from pyglet.window import key, mouse
from game import config


class Menu:
    """Main menu screen."""

    def __init__(self, window):
        """Initialize menu."""
        self.window = window
        self.selected_option = 0
        self.options = ["Start Race", "Settings", "Quit"]
        self.title = pyglet.text.Label(
            "DOG GO AROUND",
            font_size=48,
            x=config.WINDOW_WIDTH // 2,
            y=config.WINDOW_HEIGHT - 150,
            anchor_x="center",
            anchor_y="center",
            color=(255, 200, 0, 255),
        )

    def on_key_press(self, symbol):
        if symbol == key.UP:
            self.selected_option = (self.selected_option - 1) % len(self.options)
        elif symbol == key.DOWN:
            self.selected_option = (self.selected_option + 1) % len(self.options)
        elif symbol in (key.ENTER, key.SPACE):
            opt = self.options[self.selected_option]
            if opt == "Start Race":
                return "start"
            if opt == "Quit":
                return "quit"
            return "settings"
        return None

    def on_mouse_press(self, mx, my, button):
        if button != mouse.LEFT:
            return None
        for i, option in enumerate(self.options):
            option_y = config.WINDOW_HEIGHT // 2 + i * 80
            x = config.WINDOW_WIDTH // 2 - 150
            y = option_y - 30
            if x <= mx <= x + 300 and y <= my <= y + 60:
                if option == "Start Race":
                    return "start"
                if option == "Quit":
                    return "quit"
                return "settings"
        return None

    def render(self, batch):
        # Title
        self.title.draw()
        # Options (simple rectangles + labels)
        for i, option in enumerate(self.options):
            option_y = config.WINDOW_HEIGHT // 2 + i * 80
            x = config.WINDOW_WIDTH // 2 - 150
            y = option_y - 30
            width = 300
            height = 60
            # Highlight if selected
            bg = (60, 60, 100) if i == self.selected_option else (40, 40, 60)
            rect = pyglet.shapes.Rectangle(x, y, width, height, color=bg, batch=batch)
            label = pyglet.text.Label(
                option,
                font_size=24,
                x=x + width // 2,
                y=y + height // 2,
                anchor_x="center",
                anchor_y="center",
                color=(
                    (255, 255, 255, 255)
                    if i == self.selected_option
                    else (180, 180, 180, 255)
                ),
                batch=batch,
            )
