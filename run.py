"""Main entry point for Dog Go Around racing game."""

import argparse
import sys
from game.core.app import GameApp


def main():
    parser = argparse.ArgumentParser(
        description="Dog Go Around - Multiplayer Racing Game"
    )
    parser.add_argument(
        "--server",
        type=str,
        default="127.0.0.1:7777",
        help="Server address in format host:port",
    )
    parser.add_argument("--name", type=str, default="Player1", help="Player name")
    parser.add_argument("--offline", action="store_true", help="Run in offline mode")

    args = parser.parse_args()

    # Parse server address
    if ":" in args.server:
        host, port = args.server.split(":")
        port = int(port)
    else:
        host = args.server
        port = 7777

    # Start game
    app = GameApp(
        player_name=args.name,
        server_host=host,
        server_port=port,
        offline_mode=args.offline,
    )
    app.run()


if __name__ == "__main__":
    main()
