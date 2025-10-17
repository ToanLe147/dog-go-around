"""Game server with authoritative state."""

import asyncio
import argparse
import time
from typing import Dict, Set
import websockets
from game import config
from game.net.messages import (
    deserialize_message,
    serialize_message,
    StateSnapshot,
    LobbyStateMessage,
)


class Player:
    """Server-side player representation."""

    def __init__(self, player_id, name, websocket):
        self.id = player_id
        self.name = name
        self.websocket = websocket
        self.position = [0, 1, 0]
        self.rotation = [0, 0, 0]
        self.velocity = [0, 0, 0]
        self.ready = False
        self.lap = 1
        self.checkpoint = 0


class NetworkServer:
    """Authoritative game server with lobby and room management."""

    def __init__(self, host="0.0.0.0", port=7777):
        self.host = host
        self.port = port
        self.players: Dict[str, Player] = {}
        self.connected_clients: Set = set()
        self.running = False
        self.tick_rate = config.TICKRATE
        self.snapshot_rate = config.SNAPSHOT_RATE
        self.last_snapshot_time = 0
        self.player_counter = 0

    async def handle_client(self, websocket, path):
        """Handle a connected client."""
        player_id = None

        try:
            self.connected_clients.add(websocket)
            print(f"Client connected from {websocket.remote_address}")

            # Wait for join message
            data = await websocket.recv()
            message = deserialize_message(data)

            if message["type"] == "join":
                player_id = f"player_{self.player_counter}"
                self.player_counter += 1

                player_name = message["data"]["player_name"]
                player = Player(player_id, player_name, websocket)
                self.players[player_id] = player

                # Send player ID
                response = serialize_message("join_response", {"player_id": player_id})
                await websocket.send(response)

                print(f"Player {player_name} joined as {player_id}")

                # Handle player messages
                async for msg in websocket:
                    await self.handle_message(player_id, msg)

        except websockets.exceptions.ConnectionClosed:
            print(f"Client {player_id} disconnected")
        finally:
            self.connected_clients.discard(websocket)
            if player_id and player_id in self.players:
                del self.players[player_id]

    async def handle_message(self, player_id, data):
        """Handle message from player."""
        try:
            message = deserialize_message(data)
            msg_type = message["type"]
            msg_data = message["data"]

            if msg_type == "input":
                # Update player state based on input
                player = self.players.get(player_id)
                if player:
                    # Store input for processing
                    pass  # Input processing would go here

            elif msg_type == "chat":
                # Broadcast chat message
                await self.broadcast_message("chat", msg_data)

            elif msg_type == "ready":
                player = self.players.get(player_id)
                if player:
                    player.ready = msg_data.get("ready", False)

        except Exception as e:
            print(f"Error handling message: {e}")

    async def broadcast_message(self, msg_type, data):
        """Broadcast message to all connected clients."""
        if self.connected_clients:
            message = serialize_message(msg_type, data)
            await asyncio.gather(
                *[client.send(message) for client in self.connected_clients],
                return_exceptions=True,
            )

    async def game_loop(self):
        """Main game loop for state updates."""
        while self.running:
            current_time = time.time()

            # Send snapshots at configured rate
            if current_time - self.last_snapshot_time >= 1.0 / self.snapshot_rate:
                await self.send_state_snapshot()
                self.last_snapshot_time = current_time

            # Wait for next tick
            await asyncio.sleep(1.0 / self.tick_rate)

    async def send_state_snapshot(self):
        """Send game state snapshot to all clients."""
        players_data = []

        for player in self.players.values():
            players_data.append(
                {
                    "id": player.id,
                    "name": player.name,
                    "position": player.position,
                    "rotation": player.rotation,
                    "velocity": player.velocity,
                    "lap": player.lap,
                    "checkpoint": player.checkpoint,
                }
            )

        snapshot = StateSnapshot(timestamp=time.time(), players=players_data)

        await self.broadcast_message("state", snapshot)

    async def start(self):
        """Start the server."""
        self.running = True
        print(f"Starting server on {self.host}:{self.port}")

        # Start WebSocket server
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"Server listening on ws://{self.host}:{self.port}")

            # Start game loop
            await self.game_loop()


def main():
    """Main entry point for server."""
    parser = argparse.ArgumentParser(description="Dog Go Around - Game Server")
    parser.add_argument(
        "--host",
        type=str,
        default=config.DEFAULT_SERVER_HOST,
        help="Server host address",
    )
    parser.add_argument(
        "--port", type=int, default=config.DEFAULT_SERVER_PORT, help="Server port"
    )

    args = parser.parse_args()

    server = NetworkServer(args.host, args.port)

    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        print("\nServer shutting down...")


if __name__ == "__main__":
    main()
