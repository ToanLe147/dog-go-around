from ursina import *
from src.game import Game

# Global game instance
game_instance = None

def update():
    if game_instance:
        game_instance.update()

def main():
    app = Ursina()
    window.title = 'Simple 3D Game'
    window.borderless = False
    window.fullscreen = False
    window.exit_button.visible = False
    window.fps_counter.enabled = True

    global game_instance
    game_instance = Game()

    app.run()

if __name__ == '__main__':
    main()

