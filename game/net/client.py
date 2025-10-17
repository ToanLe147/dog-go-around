"""Network client for multiplayer connection."""

import asyncio
import time
from typing import Optional
import websockets
from game.net.messages import (
    serialize_message,
    deserialize_message,
    JoinMessage,
    InputMessage,
)


class NetworkClient:
    """Network client with input sending and state interpolation."""

    def __init__(self, host, port, player_name, world):
        self.host = host
        self.port = port
        self.player_name = player_name
        self.world = world
        self.websocket: Optional[websockets.WebSocketClientProtocol] = None
        self.player_id = None
        self.connected = False
        self.running = False

        # State interpolation
        self.server_states = []
        self.interpolation_delay = 0.1

        # Start connection
        asyncio.create_task(self.connect())

    async def connect(self):
        """Connect to server."""
        try:
            uri = f"ws://{self.host}:{self.port}"
            print(f"Connecting to {uri}...")

            self.websocket = await websockets.connect(uri)

            # Send join message
            join_msg = JoinMessage(player_name=self.player_name)
            await self.websocket.send(serialize_message("join", join_msg))

            # Wait for join response
            response = await self.websocket.recv()
            message = deserialize_message(response)

            if message["type"] == "join_response":
                self.player_id = message["data"]["player_id"]
                self.connected = True
                self.running = True
                print(f"Connected as {self.player_id}")

                # Start receive loop
                asyncio.create_task(self.receive_loop())

        except Exception as e:
            print(f"Connection error: {e}")
            self.connected = False

    async def receive_loop(self):
        """Receive messages from server."""
        try:
            async for message_data in self.websocket:
                message = deserialize_message(message_data)
                await self.handle_message(message)
        except Exception as e:
            print(f"Receive error: {e}")
            self.connected = False

    async def handle_message(self, message):
        """Handle message from server."""
        msg_type = message["type"]
        msg_data = message["data"]

        if msg_type == "state":
            # Store state snapshot for interpolation
            self.server_states.append(
                {"timestamp": msg_data["timestamp"], "players": msg_data["players"]}
            )

            # Keep only recent states
            if len(self.server_states) > 10:
                self.server_states.pop(0)

        elif msg_type == "chat":
            print(f"[Chat] {msg_data['player_name']}: {msg_data['message']}")

    def update(self):
        """Update client state (called from game loop)."""
        if not self.connected:
            return

        # Send input to server
        if self.world and self.world.player_car:
            asyncio.create_task(self.send_input())

        # Interpolate remote players
        self.interpolate_state()

    async def send_input(self):
        """Send player input to server."""
        if not self.websocket or not self.player_id:
            return

        car = self.world.player_car

        # Get current input state
        throttle = 0.0
        steer = 0.0
        brake = False
        handbrake = False
        boost = False

        # This would come from actual input
        # For now, placeholder

        input_msg = InputMessage(
            player_id=self.player_id,
            throttle=throttle,
            steer=steer,
            brake=brake,
            handbrake=handbrake,
            boost=boost,
            timestamp=time.time(),
        )

        try:
            await self.websocket.send(serialize_message("input", input_msg))
        except Exception as e:
            print(f"Error sending input: {e}")

    def interpolate_state(self):
        """Interpolate remote player positions."""
        if len(self.server_states) < 2:
            return

        render_time = time.time() - self.interpolation_delay

        # Find two states to interpolate between
        for i in range(len(self.server_states) - 1):
            if (
                self.server_states[i]["timestamp"]
                <= render_time
                <= self.server_states[i + 1]["timestamp"]
            ):

                state0 = self.server_states[i]
                state1 = self.server_states[i + 1]

                # Calculate interpolation factor
                time_diff = state1["timestamp"] - state0["timestamp"]
                if time_diff > 0:
                    t = (render_time - state0["timestamp"]) / time_diff

                    # Interpolate each player
                    for player_data in state1["players"]:
                        player_id = player_data["id"]

                        # Skip local player
                        if player_id == self.player_id:
                            continue

                        # Find corresponding player in previous state
                        prev_player = next(
                            (p for p in state0["players"] if p["id"] == player_id), None
                        )

                        if prev_player and self.world:
                            # Interpolate position
                            pos = self.lerp_vec3(
                                prev_player["position"], player_data["position"], t
                            )

                            # Update or create remote car
                            if player_id not in self.world.other_cars:
                                self.world.add_car(
                                    player_id, pos, player_data["rotation"]
                                )
                            else:
                                self.world.other_cars[player_id].set_position(pos)

    def lerp_vec3(self, a, b, t):
        """Linear interpolation between two 3D vectors."""
        return [
            a[0] + (b[0] - a[0]) * t,
            a[1] + (b[1] - a[1]) * t,
            a[2] + (b[2] - a[2]) * t,
        ]

    def disconnect(self):
        """Disconnect from server."""
        self.running = False
        if self.websocket:
            asyncio.create_task(self.websocket.close())
