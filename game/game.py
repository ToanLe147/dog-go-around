"""Main game application with Pygame."""

import pygame
import sys
from game import config


class Game:
    """Main game class."""

    def __init__(self, offline_mode=False, player_name="Player1"):
        """Initialize the game."""
        pygame.init()

        # Set up display
        flags = pygame.FULLSCREEN if config.FULLSCREEN else 0
        self.screen = pygame.display.set_mode(
            (config.WINDOW_WIDTH, config.WINDOW_HEIGHT), flags
        )
        pygame.display.set_caption(config.WINDOW_TITLE)

        # Clock for managing FPS
        self.clock = pygame.time.Clock()

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
        self.menu = Menu(self.screen)
        self.hud = HUD(self.screen)
        self.cars = [self.player_car]

        # Camera offset for following player
        self.camera_x = 0
        self.camera_y = 0

    def run(self):
        """Main game loop."""
        while self.running:
            dt = self.clock.tick(config.FPS) / 1000.0  # Delta time in seconds

            self.handle_events()
            self.update(dt)
            self.render()

        pygame.quit()
        sys.exit()

    def handle_events(self):
        """Handle user input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if self.state == "menu":
                action = self.menu.handle_event(event)
                if action == "start":
                    self.start_race()
                elif action == "quit":
                    self.running = False

            elif self.state == "racing":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "paused"

            elif self.state == "paused":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.state = "racing"
                    elif event.key == pygame.K_q:
                        self.state = "menu"

    def update(self, dt):
        """Update game logic."""
        if self.state == "racing":
            # Get input
            keys = pygame.key.get_pressed()

            # Update player car
            self.player_car.update(dt, keys, self.track)

            # Update camera to follow player
            self.camera_x = self.player_car.x - config.WINDOW_WIDTH // 2
            self.camera_y = self.player_car.y - config.WINDOW_HEIGHT // 2

            # Update HUD
            self.hud.update(self.player_car)

    def render(self):
        """Render the game."""
        self.screen.fill(config.COLOR_BACKGROUND)

        if self.state == "menu":
            self.menu.render()

        elif self.state in ["racing", "paused"]:
            # Render track with camera offset
            self.track.render(self.screen, self.camera_x, self.camera_y)

            # Render cars
            for car in self.cars:
                car.render(self.screen, self.camera_x, self.camera_y)

            # Render HUD
            self.hud.render()

            # Render pause overlay
            if self.state == "paused":
                self.render_pause_overlay()

        pygame.display.flip()

    def start_race(self):
        """Start a new race."""
        self.state = "racing"
        self.player_car.reset(100, 100)

    def render_pause_overlay(self):
        """Render pause menu overlay."""
        # Semi-transparent overlay
        overlay = pygame.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Pause text
        font = pygame.font.Font(None, 74)
        text = font.render("PAUSED", True, config.COLOR_TEXT)
        text_rect = text.get_rect(
            center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 - 50)
        )
        self.screen.blit(text, text_rect)

        # Instructions
        font_small = pygame.font.Font(None, 36)
        resume_text = font_small.render("Press ESC to resume", True, config.COLOR_TEXT)
        resume_rect = resume_text.get_rect(
            center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 20)
        )
        self.screen.blit(resume_text, resume_rect)

        quit_text = font_small.render(
            "Press Q to quit to menu", True, config.COLOR_TEXT
        )
        quit_rect = quit_text.get_rect(
            center=(config.WINDOW_WIDTH // 2, config.WINDOW_HEIGHT // 2 + 60)
        )
        self.screen.blit(quit_text, quit_rect)
