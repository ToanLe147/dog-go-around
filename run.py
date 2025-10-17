"""Entry point for Dog Go Around racing game."""

import argparse
from game.game import Game


def main():
    """Parse arguments and start the game."""
    parser = argparse.ArgumentParser(description="Dog Go Around - Racing Game")
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Run in offline mode (no multiplayer)",
    )
    parser.add_argument(
        "--name",
        type=str,
        default="Player1",
        help="Player name",
    )
    parser.add_argument(
        "--server",
        type=str,
        default="127.0.0.1:7777",
        help="Server address (host:port)",
    )
    
    args = parser.parse_args()
    
    # Start the game
    game = Game(
        offline_mode=args.offline,
        player_name=args.name
    )
    game.run()


if __name__ == "__main__":
    main()
