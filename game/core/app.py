"""Main game application class."""

from ursina import *
from game import config
from game.core.world import World
from game.core.race import RaceManager
from game.core.camera_rig import CameraRig
from game.core.hud import HUD
from game.ui.menu import MainMenu
from game.ui.pause_menu import PauseMenu
from game.ui.results import ResultsScreen
from game.net.client import NetworkClient


class GameApp:
    """Main application class that bootstraps and manages the game."""

    def __init__(
        self,
        player_name="Player1",
        server_host="127.0.0.1",
        server_port=7777,
        offline_mode=False,
    ):
        """Initialize the game application."""
        self.player_name = player_name
        self.server_host = server_host
        self.server_port = server_port
        self.offline_mode = offline_mode

        # Initialize Ursina
        self.app = Ursina(
            title=config.WINDOW_TITLE,
            borderless=config.WINDOW_BORDERLESS,
            fullscreen=config.WINDOW_FULLSCREEN,
            development_mode=config.DEBUG_MODE,
        )

        # Set window properties
        window.size = (config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
        window.fps_counter.enabled = config.SHOW_FPS
        window.exit_button.visible = False

        # Game state
        self.state = "menu"  # menu, lobby, racing, paused, results
        self.world = None
        self.race_manager = None
        self.camera_rig = None
        self.hud = None
        self.network_client = None

        # UI screens
        self.main_menu = MainMenu(self)
        self.pause_menu = PauseMenu(self)
        self.results_screen = ResultsScreen(self)

        # Show main menu
        self.show_menu()

        # Set up update loop
        self.app.update = self.update

    def update(self):
        """Called every frame."""
        if self.state == "racing":
            if self.world:
                self.world.update()
            if self.race_manager:
                self.race_manager.update()
            if self.camera_rig:
                self.camera_rig.update()
            if self.hud:
                self.hud.update()
            if self.network_client:
                self.network_client.update()

            # Check for pause
            if held_keys["escape"]:
                self.pause_game()

    def show_menu(self):
        """Show main menu."""
        self.state = "menu"
        self.main_menu.show()
        if self.pause_menu:
            self.pause_menu.hide()
        if self.results_screen:
            self.results_screen.hide()

    def start_race(self, track_name="default"):
        """Start a new race."""
        self.state = "racing"
        self.main_menu.hide()

        # Create world
        self.world = World(track_name)

        # Create race manager
        self.race_manager = RaceManager(self.world)

        # Create camera
        self.camera_rig = CameraRig(self.world.player_car)

        # Create HUD
        self.hud = HUD(self.race_manager)

        # Connect to server if not offline
        if not self.offline_mode:
            self.network_client = NetworkClient(
                self.server_host, self.server_port, self.player_name, self.world
            )

    def pause_game(self):
        """Pause the game."""
        if self.state == "racing":
            self.state = "paused"
            self.pause_menu.show()
            application.paused = True

    def resume_game(self):
        """Resume the game."""
        if self.state == "paused":
            self.state = "racing"
            self.pause_menu.hide()
            application.paused = False

    def show_results(self, results_data):
        """Show race results."""
        self.state = "results"
        self.results_screen.show(results_data)

    def quit_game(self):
        """Quit the game."""
        if self.network_client:
            self.network_client.disconnect()
        application.quit()

    def run(self):
        """Start the game loop."""
        self.app.run()
